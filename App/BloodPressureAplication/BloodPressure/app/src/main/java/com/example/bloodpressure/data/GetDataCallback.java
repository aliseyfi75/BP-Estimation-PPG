package com.example.bloodpressure.data;

public interface GetDataCallback<Data> {
    void onSuccess(Data data);
    void onFail(int errorCode, String error);
}
