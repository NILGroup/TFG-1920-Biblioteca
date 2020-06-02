
/*
 * Book.java
 * Created by Jose Luis Moreno on 5/11/19 9:49 PM
 * MIT License
 * Copyright (c) 2019 . Mauricio Abbati Loureiro - Jose Luis Moreno Varillas
 * Last modified 5/5/19 1:15 PM
 */

package ucm.fdi.android.speechtotext.Items;

import java.net.URL;
import java.util.ArrayList;

public class Book {
    private String title;
    private String author;
    private ArrayList<String> isbnList;
    private String oclc;
    private String available;
    private String url;

    public Book(String _title, String _author, ArrayList<String> _isbnList, String _oclc){
        title = _title;
        author = _author;
        isbnList = _isbnList;
        available = "";
        url = "";
        oclc = _oclc;
    }

    public Book(String _title, String _author, String _oclc){
        title = _title;
        author = _author;
        isbnList = new ArrayList<>();
        available = "";
        url = "";
        oclc = _oclc;
    }

    public Book(String _title, String _author, ArrayList<String> _isbnList, String _available, String _url, String _oclc) {
        title = _title;
        author = _author;
        isbnList = _isbnList;
        available = _available;
        url = _url;
        oclc = _oclc;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public ArrayList<String> getISBNList() {
        return isbnList;
    }

    public void setISBNList(ArrayList<String> isbnCode) {
        this.isbnList = isbnCode;
    }

    public String getAvailable(){
        return this.available;
    }

    public void setAvailable(String available){
        this.available = available;
    }

    public String getUrl(){return this.url;}

    public void setUrl(String url){this.url = url;}

    public String getOCLC(){return this.oclc;}

    public void setOCLC(String oclc){this.oclc = url;}
}
