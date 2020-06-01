/*
 * CustomPreferenceFragment.java
 * Created by Jose Luis Moreno on 30/05/20 19:46
 * MIT License
 * Copyright (c) 2020 . Mauricio Abbati Loureiro - Jose Luis Moreno Varillas
 * Last modified 30/05/20 19:46
 */

package ucm.fdi.android.speechtotext;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.Preference;
import android.preference.PreferenceFragment;

public class CustomPreferenceFragment extends PreferenceFragment implements SharedPreferences.OnSharedPreferenceChangeListener
{
    @Override
    public void onCreate(final Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        addPreferencesFromResource(R.xml.preference_screen);
    }

    @Override
    public void onResume() {
        super.onResume();
        getPreferenceScreen().getSharedPreferences().registerOnSharedPreferenceChangeListener(this);
    }

    @Override
    public void onPause() {
        super.onPause();
        getPreferenceScreen().getSharedPreferences().unregisterOnSharedPreferenceChangeListener(this);
    }

    @Override
    public void onSharedPreferenceChanged(SharedPreferences sharedPreferences, String key)
    {
        if (key.equals("setting_title_font_color"))
        {
            Preference pref = findPreference(key);
        }
    }
}
