(defvar icalang-mode-hook nil)

(defvar icalang-keywords
  '("import" "def" "end" "fun" "while" "if" "show" "print" "pop" "pops"
    "strtostack" "==" "!=" "===" "!==" "stopwhile" "+" "-" "stk" ">=" "<=" 
    "dup" ">" "<" "not" "nothing" "split" "argv0" "argv1" "argv2" "argv3"
    "strstack" "add" "sub" "stop"))

(defvar icalang-font-lock-keywords
  (let* (
         (x-keywords (regexp-opt icalang-keywords 'words))
         )
    `(
      (,x-keywords . font-lock-keyword-face)
      )))

(defvar icalang-mode-syntax-table
  (let ((syntax-table (make-syntax-table)))
    (modify-syntax-entry ?/ ". 124b" syntax-table)
    (modify-syntax-entry ?* ". 23" syntax-table)
    (modify-syntax-entry ?\n ">" syntax-table)
    syntax-table)
  "Syntax table for icalang-mode")

;; Função principal para iniciar o modo maior
(defun icalang-mode ()
  "Larger mode to edit Icalang files."
  (interactive)
  (kill-all-local-variables)
  (set-syntax-table icalang-mode-syntax-table)
  (set (make-local-variable 'font-lock-defaults) '(icalang-font-lock-keywords))
  (set (make-local-variable 'indent-line-function) 'indent-relative)
  (setq major-mode 'icalang-mode)
  (setq mode-name "Icalang")
  (run-hooks 'icalang-mode-hook))

(add-to-list 'auto-mode-alist '("\\.icaro\\'" . icalang-mode))

(provide 'icalang-mode)
