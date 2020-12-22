package com.example.bloodpressure.handler;


import android.util.Log;
import android.webkit.MimeTypeMap;

import com.example.bloodpressure.data.GetDataCallback;
import com.example.bloodpressure.data.request.StatusRequest;
import com.example.bloodpressure.data.response.SimpleResponse;
import com.example.bloodpressure.util.IP_Holder;
import com.google.gson.Gson;

import org.androidannotations.annotations.Background;
import org.androidannotations.annotations.EBean;
import org.androidannotations.annotations.UiThread;

import java.io.File;
import java.io.IOException;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import okhttp3.ResponseBody;

@EBean(scope = EBean.Scope.Singleton)
public class ServerHandler {

    private String mainServerUrl;

    public static final MediaType MEDIA_TYPE_MARKDOWN = MediaType.parse("text/x-markdown; charset=utf-8");
    public static final MediaType JSON_TYPE = MediaType.parse("application/json; charset=utf-8");
    private static final MediaType MEDIA_TYPE_PNG = MediaType.parse("image/png");
    private static final MediaType MEDIA_TYPE_JPG = MediaType.parse("image/jpg");
    private static final MediaType MEDIA_TYPE_FILE = MediaType.parse("multipart/form-data");

    private final OkHttpClient client = new OkHttpClient();
    private static long sequenceNumber = 0;

    public static long getSequenceNumber() {
        return sequenceNumber;
    }

    public static void setSequenceNumber(long sequenceNumber) {
        ServerHandler.sequenceNumber = sequenceNumber;
    }

    @Background
    public void uploadFile(String fileName, GetDataCallback<SimpleResponse> callback){
        mainServerUrl = "http://"+IP_Holder.getIp()+":5000";
        File videoFile  = new File(fileName);
        RequestBody requestBody = new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("file", videoFile.getName(),
                        RequestBody.create(MEDIA_TYPE_FILE, videoFile))
                .build();

        Request request = new Request.Builder()
                .url(mainServerUrl)
                .post(requestBody)
                .build();
        try {
            Response response = client.newCall(request).execute();
            if (!response.isSuccessful()){
                onFail(callback,response);
            }
            else{
                ResponseBody responseBody = response.body();
                if(responseBody==null)
                    onFail(callback);
                else{
                    SimpleResponse code = new Gson().fromJson(responseBody.string(),SimpleResponse.class);
                    onSuccess(callback,code);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
            onFail(callback,e);
        }
    }

    @UiThread
    protected void onSuccess(GetDataCallback callback , Object data){
        if(callback!=null)
            callback.onSuccess(data);
    }

    @UiThread
    protected void onFail(GetDataCallback callback , int code , String message){
        if(callback!=null)
            callback.onFail(code,message);
    }

    protected void onFail(GetDataCallback callback){
        onFail(callback,500,"Unknown error");
    }

    protected void onFail(GetDataCallback callback , Response response){
        if(response!=null)
            onFail(callback,response.code(),response.message());
        else
            onFail(callback);
    }

    protected void onFail(GetDataCallback callback , Exception e){
        if(e!=null)
            onFail(callback,500,e.getMessage());
        else
            onFail(callback,500,"Unknown error");
    }

}
