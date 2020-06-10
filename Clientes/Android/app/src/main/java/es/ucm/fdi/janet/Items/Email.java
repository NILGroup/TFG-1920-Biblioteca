/*
 * Email.java
 * Created by Miguel Ángel Castillo Moreno on 23/05/20 13:26
 * MIT License
 * Copyright (c) 2019 . Mauricio Abbati Loureiro - Jose Luis Moreno Varillas
 * Last modified 23/05/20 13:26
 */

package es.ucm.fdi.janet.Items;

public class Email {
    private String email;
    private String library;

    public Email(String email, String library) {
        this.email = email;
        this.library = library;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getLibrary() {
        return library;
    }

    public void setLibrary(String library) {
        this.library = library;
    }
}
