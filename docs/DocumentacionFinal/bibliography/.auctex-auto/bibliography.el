;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "bibliography"
 (lambda ()
   (LaTeX-add-bibitems
    "tuxilo-github"
    "postgis"
    "libreoffice_calc"
    "gnu_emacs"
    "openstreetmap_about"
    "gnu_bash"
    "odbl_license"
    "wiki_geojson"
    "leafletjs"))
 '(or :bibtex :latex))

