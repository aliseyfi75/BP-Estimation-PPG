package com.example.bloodpressure.util;

import android.content.SharedPreferences;
import android.preference.PreferenceManager;

public class IP_Holder {
    private static SharedPreferences preferences = PreferenceManager.getDefaultSharedPreferences(App.getContext());
    private static String ip;

    public static String getIp() {
        ip = preferences.getString("IP","");
        return ip;
    }

    public static void setIp(String s) {
        SharedPreferences.Editor editor = preferences.edit();
        editor.putString("IP",s);
        editor.apply();
        ip = s;
    }
}
