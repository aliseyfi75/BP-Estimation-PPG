package com.example.bloodpressure.activity;

import android.os.Build;
import android.os.Bundle;

import androidx.annotation.IdRes;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import com.example.bloodpressure.interfaces.OnBackPressedListener;

import org.androidannotations.annotations.EActivity;
import org.androidannotations.annotations.UiThread;

import java.util.List;


@EActivity
public class BaseActivity extends AppCompatActivity {

    @UiThread
    public void addPage(Fragment fragment, @IdRes int pager, @Nullable String tag){
        FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        assert fragment!=null;
        ft.replace(pager, fragment, tag);
        ft.addToBackStack(null);
        ft.commit();
    }
    @UiThread
    public void addPage(Class<? extends Fragment> page, Bundle bundle, @IdRes int pager, @Nullable String tag){
        Fragment fragment = null;
        try {
            fragment = page.newInstance();
        } catch (InstantiationException e) {
            e.printStackTrace();
        } catch ( IllegalAccessException e ) {
            e.printStackTrace();
        }
        if(fragment != null) {
            fragment.setArguments(bundle);
        }
        addPage(fragment,pager, tag);
    }

    @UiThread
    public void newPage(Fragment fragment, @IdRes int pager, @Nullable String tag){
        FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        assert fragment!=null;
        while (getSupportFragmentManager().getBackStackEntryCount() > 0){
            getSupportFragmentManager().popBackStackImmediate();
        }
        ft.replace(pager, fragment, tag);
        ft.commit();
    }

    @UiThread
    public void newPage(Fragment fragment, @IdRes int pager, @Nullable String tag, int enterAnim, int exitAnim){
        FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        assert fragment!=null;
        while (getSupportFragmentManager().getBackStackEntryCount() > 0){
            getSupportFragmentManager().popBackStackImmediate();
        }
        ft.setCustomAnimations(enterAnim, exitAnim);
        ft.replace(pager, fragment, tag);
        ft.commit();
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    @UiThread
    public void newPage(Class<? extends Fragment> page, Bundle bundle, @IdRes int pager, @Nullable String tag){
        Fragment fragment = null;
        try {
            fragment = page.newInstance();
        } catch (InstantiationException | IllegalAccessException e) {
            e.printStackTrace();
        }
        if(fragment != null) {
            fragment.setArguments(bundle);
        }
        newPage(fragment,pager, tag);
    }

    @UiThread
    public void replacePage(Fragment fragment, @IdRes int pager, @Nullable String tag){
        FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        assert fragment!=null;
        getSupportFragmentManager().popBackStackImmediate();
        ft.replace(pager, fragment, tag);
        ft.addToBackStack(null);
        ft.commit();
    }
    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    @UiThread
    public void replacePage(Class<? extends Fragment> page, Bundle bundle, @IdRes int pager, @Nullable String tag){
        Fragment fragment = null;
        try {
            fragment = page.newInstance();
        } catch (InstantiationException | IllegalAccessException e) {
            e.printStackTrace();
        }
        if(fragment != null) {
            fragment.setArguments(bundle);
        }
        replacePage(fragment,pager, tag);
    }

    @UiThread
    public void addPageWithoutBackstack(Fragment fragment, @IdRes int pager, @Nullable String tag){
        FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        assert fragment!=null;
        ft.replace(pager, fragment, tag);
        ft.commit();
    }
    @UiThread
    public void addPageWithoutBackstack(Class<? extends Fragment> page, Bundle bundle, @IdRes int pager, @Nullable String tag){
        Fragment fragment = null;
        try {
            fragment = page.newInstance();
        } catch (InstantiationException e) {
            e.printStackTrace();
        } catch ( IllegalAccessException e ) {
            e.printStackTrace();
        }
        if(fragment != null) {
            fragment.setArguments(bundle);
        }
        addPageWithoutBackstack(fragment,pager, tag);
    }

    @UiThread
    public void backPage(){
        getSupportFragmentManager().popBackStackImmediate();
    }

    @UiThread
    public void hideFragment(Fragment fragment){
        getSupportFragmentManager().beginTransaction().hide(fragment).commit();
    }

    @UiThread
    public void showFragment(Fragment fragment){
        getSupportFragmentManager().beginTransaction().show(fragment).commit();
    }

    @UiThread
    @Override
    public void onBackPressed() {
        FragmentManager fragmentManager = getSupportFragmentManager();
        List<Fragment> fragments = fragmentManager.getFragments();
        if(fragments != null){
            for (int i = fragments.size() - 1; i >= 0 ; i--){
                Fragment fragment = fragments.get(i);
                if(fragment instanceof OnBackPressedListener && fragment.isVisible()){
                    if(((OnBackPressedListener)fragment).onBackPressed()){
                        return;
                    }
                }
            }
        }
        if(fragmentManager.getBackStackEntryCount() > 0) {
            fragmentManager.popBackStackImmediate();
            return; // FIXME: 3/29/17 check it
        }

//        long now = TimeHelper.getCurrentTime().getTime();
//        if(isTaskRoot() &&
//                now - lastBackClickTime > DOUBLE_BACK_EXIT_INTERVAL){
//            Do.toast(R.string.back_again_to_exit);
//            lastBackClickTime = now;
//            return;
//        }
        super.onBackPressed();
    }
}
