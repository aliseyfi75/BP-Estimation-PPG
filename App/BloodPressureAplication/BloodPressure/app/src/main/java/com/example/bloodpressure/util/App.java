package com.example.bloodpressure.util;

import android.app.Activity;
import android.app.Application;
import android.content.Context;
import android.os.Bundle;

public class App extends Application {
    private static Context mContext;
    private static Activity currentActivity;
    private static long id=0;

    @Override
    public void onCreate() {
        super.onCreate();
        mContext = getApplicationContext();

        registerActivityLifecycleCallbacks(new ActivityLifecycleCallbacks() {
            @Override
            public void onActivityCreated(Activity activity, Bundle savedInstanceState) {
                currentActivity = activity;
            }

            @Override
            public void onActivityStarted(Activity activity) {
                currentActivity = activity;
            }

            @Override
            public void onActivityResumed(Activity activity) {
                currentActivity = activity;
            }

            @Override
            public void onActivityPaused(Activity activity) {
            }

            @Override
            public void onActivityStopped(Activity activity) {
            }

            @Override
            public void onActivitySaveInstanceState(Activity activity, Bundle outState) {
            }

            @Override
            public void onActivityDestroyed(Activity activity) {
            }
        });

    }

    public static long getId() {
        id++;
        return id;
    }

    public static Context getContext() {
        return mContext;
    }


    public static Activity getCurrentActivity() {
        return currentActivity;
    }
}
