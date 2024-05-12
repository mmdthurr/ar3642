package main

import (
	// "flag"

	"fmt"
	"io"
	"net/http"
	"os"
)

func main() {
	// public_html_dir := flag.String("ph","/var/www/public_html","html file lists")
	// flag.Parse()

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "../html/editor.html")
	})
	http.HandleFunc("/upload", func(w http.ResponseWriter, r *http.Request) {
		bd, _ := io.ReadAll(r.Body)
		h, _ := os.Create(fmt.Sprintf("%s.html",r.Header.Get("title")))
		h.Write(bd)
		w.WriteHeader(200)
		
	})
	http.ListenAndServe("127.0.0.1:5252", nil)

}
