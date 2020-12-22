package com.example.bloodpressure.activity;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.MenuItem;
import android.widget.TextView;

import com.example.bloodpressure.R;

public class HelpActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_help);

        // Up button
        ActionBar ab= getSupportActionBar();
        ab.setDisplayHomeAsUpEnabled(true);

        TextView infoWindow = (TextView) findViewById(R.id.txtInfo);

        StringBuilder stringBuilder = new StringBuilder();

        stringBuilder.append("Developers: Ali Seyfi & Sahar Mavali\n\n");
        stringBuilder.append("Welcome to Blood Pressure Estimation App!\n\n" +
                "This application will estimate blood pressure\n" +
                "from PPG Signals extracted from users's video.\n" +
                "The process starts by clicking 'Set IP' on Main\n" +
                "Menu.\n" +
                "Type your laptop's network IPv4 address and\n" +
                "after confirming that, click on 'Take Blood \n" +
                "Pressure' to start recording a 1 minute video. \n" +
                "For recording the video, you should put your \n" +
                "finger on the lens of camera to cover it \n" +
                "completely. Then you should confirm the video, \n" +
                "and wait for the estimation to be done!\n\n" +
                "The blood pressure result will be shown on \n" +
                "the screen!" +
                "\n\n\n");

        infoWindow.setText(stringBuilder.toString());
    }

    public static Intent makeLaunchIntent(Context context) {
        return (new Intent(context, HelpActivity.class));
    }



    // Up button
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK ) {
            finish();
        }
        return super.onKeyDown(keyCode, event);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        switch (item.getItemId()){
            case android.R.id.home:
                finish();
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }
}