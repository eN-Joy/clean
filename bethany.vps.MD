apt install bash-completion git python3.8 python3.8-dev python3.8-dbg python3.8-venv command-not-found software-properties-common curl postgresql libpq-dev

.tmux.conf

irssi eN_Joy:kraettli

    (setq package-archives '(("gnu"           . "http://elpa.gnu.org/packages/")
                            ("melpa-stable" . "http://stable.melpa.org/packages/")
                            ("melpa"        . "http://melpa.org/packages/")))

    (package-initialize)

    (use-package lsp-pyright
    :ensure t
    :hook (python-mode . (lambda ()
                            (require 'lsp-pyright)
                            (lsp))))  ; or lsp-deferred
    (setq lsp-enable-file-watchers nil)

    (use-package moe-theme
    :ensure t)
    (moe-dark)
