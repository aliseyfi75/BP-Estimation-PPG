package com.example.bloodpressure.activity;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.DialogFragment;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;

import com.example.bloodpressure.R;
import com.example.bloodpressure.dialouge.IpDialog;
import com.example.bloodpressure.util.App;

import org.androidannotations.annotations.AfterViews;
import org.androidannotations.annotations.EActivity;
import org.androidannotations.annotations.ViewById;

@EActivity(R.layout.activity_main)
public class MainActivity extends BaseActivity {
    @ViewById(R.id.btn_camera)
    Button btnMoveToCameraActivity;
    @ViewById(R.id.btn_help)
    Button btnMoveToHelpActivity;
    @ViewById(R.id.btn_ip)
    Button btnIPdialog;
    @AfterViews
    void initButtons(){


        btnMoveToCameraActivity.setOnClickListener(v -> {
            Intent intent = new Intent(this,CameraActivity_.class);
            startActivity(intent);
        });

        btnMoveToHelpActivity.setOnClickListener(v -> {
            Intent intent = new Intent(this,HelpActivity.class);
            startActivity(intent);
        });

        btnIPdialog.setOnClickListener(v -> {
            DialogFragment newFragment = new IpDialog();
            newFragment.show(getSupportFragmentManager(), "missiles");
        });
    }
    public static Intent makeLaunchIntent(Context context){
        return (new Intent(context, MainActivity.class));
    }

}