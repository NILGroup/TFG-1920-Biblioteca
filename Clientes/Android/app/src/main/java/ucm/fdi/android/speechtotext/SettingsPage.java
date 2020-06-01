/*
 * SettingsPage.java
 * Created by Jose Luis Moreno on 30/05/20 19:50
 * MIT License
 * Copyright (c) 2020 . Mauricio Abbati Loureiro - Jose Luis Moreno Varillas
 * Last modified 30/05/20 19:50
 */

package ucm.fdi.android.speechtotext;

import android.os.Bundle;
import android.preference.PreferenceActivity;

public class SettingsPage extends PreferenceActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getFragmentManager().beginTransaction().replace(android.R.id.content, new CustomPreferenceFragment()).commit();
    }
}
