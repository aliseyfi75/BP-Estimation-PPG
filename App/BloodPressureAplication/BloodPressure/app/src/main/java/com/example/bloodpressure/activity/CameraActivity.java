package com.example.bloodpressure.activity;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.view.KeyEvent;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.example.bloodpressure.R;
import com.example.bloodpressure.data.GetDataCallback;
import com.example.bloodpressure.data.response.SimpleResponse;
import com.example.bloodpressure.handler.ServerHandler;
import com.example.bloodpressure.util.App;

import org.androidannotations.annotations.AfterViews;
import org.androidannotations.annotations.Bean;
import org.androidannotations.annotations.EActivity;
import org.androidannotations.annotations.ViewById;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;

import wseemann.media.FFmpegMediaMetadataRetriever;

@EActivity(R.layout.activity_camera)
public class CameraActivity extends BaseActivity {


    @Bean
    ServerHandler serverHandler;
    @ViewById(R.id.btn_record)
    Button btnRecord;
    @ViewById(R.id.hbr)
    TextView hbr_tv;
    private String hbr_value;

    public static Intent makeLaunchIntent(Context context) {
        return (new Intent(context, CameraActivity.class));
    }
    @AfterViews
    void init(){
        hbr_tv.setVisibility(View.INVISIBLE);
        int writeExternalStoragePermission = ContextCompat.checkSelfPermission(App.getContext(), Manifest.permission.WRITE_EXTERNAL_STORAGE);
        if(writeExternalStoragePermission!= PackageManager.PERMISSION_GRANTED)
        {
            ActivityCompat.requestPermissions(App.getCurrentActivity(), new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 0);
        }

        setUpButtonRecord();

    }
    private void setUpButtonRecord(){
        btnRecord.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
                // Duration limitation

                File mediaFile = getOutputMediaFile();
                Log.d("SHIT", "onClick: "+App.getContext()+
                        "com.example.bloodpressure"+ ".provider");
                Uri output = FileProvider.getUriForFile(
                        App.getContext(),
                        "com.example.bloodpressure" + ".provider",
                        mediaFile);
                intent.putExtra(MediaStore.EXTRA_OUTPUT, output);
                intent.putExtra(MediaStore.EXTRA_DURATION_LIMIT, 60);
                startActivityForResult(intent,1);
            }
        });
    }
    private static File getOutputMediaFile(){
        File mediaStorageDir = new File(Environment.getExternalStorageDirectory()
                + "/BloodPressure");
        if (! mediaStorageDir.exists()){
            if (! mediaStorageDir.mkdirs()){
                return null;
            }
        }
        String mVidName="VI_BP.mp4";
        File vidFile = new File(mediaStorageDir.getPath() + File.separator + mVidName);
        return vidFile;
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        Log.d("SHIT", "onActivityResult: "+ data);

        if (resultCode == RESULT_OK && requestCode == 1){
            if (resultCode == RESULT_OK){
                hbr_tv.setVisibility(View.INVISIBLE);
                Toast.makeText(getApplicationContext(), "Video Successfully Recorded", Toast.LENGTH_SHORT).show();
                String vidFileAddress = Environment.getExternalStorageDirectory()
                        + "/BloodPressure/VI_BP.mp4";
                serverHandler.uploadFile(vidFileAddress, new GetDataCallback<SimpleResponse>() {
                    @Override
                    public void onSuccess(SimpleResponse simpleResponse) {
                        hbr_value = simpleResponse.getCode();
                        hbr_tv.setText(hbr_value);
                        hbr_tv.setVisibility(View.VISIBLE);
                    }

                    @Override
                    public void onFail(int errorCode, String error) {

                    }
                });



            } else {
                Toast.makeText(getApplicationContext(), "Video Capture Failed", Toast.LENGTH_SHORT).show();
            }
        }
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