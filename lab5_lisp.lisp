;;;import of modeule for reading csv-files
(require "cl-csv")

;;;path of file with statistics
(defparameter data (cl-csv:read-csv #P"C:/Users/lenovo/pythonLabs/PacMan-1/statistics.csv"))

;;;lists for needed string values from statistics
(defparameter listOfMinimaxes ())
(defparameter timeAsString ())
(defparameter scoreAsString ())

;;;lists for converted to numbers values
(defparameter timeAsNumber ())
(defparameter scoreAsNumber ())

;;;initializing of variable for finding values
(defparameter matSpodForTime 0)
(defparameter matSpodForScore 0)
(defparameter dysperseForScore 0)

;;;reading, finding and collecting data about minimax algorythm
(loop for item in data
   do (if (string-equal (NTH 3 item) "minimax")
             (push item listOfMinimaxes)))

;;;selecting of time as string
(loop for item in listOfMinimaxes
   do (push (String-left-trim "0:00:" (NTH 1 item)) timeAsString))

;;;selecting of score as string
(loop for item in listOfMinimaxes
   do (push (NTH 2 item) scoreAsString))

;;;converting to number type of time
(loop for item in timeAsString
   do (push (NTH 0 (with-input-from-string (in item)
  (loop for x = (read in nil nil) while x collect x))) timeAsNumber))

;;;converting to number type of time
(loop for item in scoreAsString
   do (push (NTH 0 (with-input-from-string (in item)
  (loop for x = (read in nil nil) while x collect x))) scoreAsNumber))

;;;calculating and setting of values for mean of time
(setq matSpodForTime (/ (float (apply '+ timeAsNumber)) (length timeAsNumber)))
(print "Математичне сподівання для часу:") 
(write matSpodForTime) 

;;;calculating and setting of values for mean of score
(setq matSpodForScore (/ (float(apply '+ scoreAsNumber)) (length scoreAsNumber)))
(print "Математичне сподівання для рахунку:") 
(write matSpodForScore)

;;;calculating and setting of values for dysperse of score
(setq dysperseForScore (/ (apply '+ (mapcar (lambda (x) (* x x)) (mapcar (lambda (n) (- n matSpodForScore))
        scoreAsNumber))) (length scoreAsNumber)))
(print "Дисперсія для рахунку:") 
(write dysperseForScore)


