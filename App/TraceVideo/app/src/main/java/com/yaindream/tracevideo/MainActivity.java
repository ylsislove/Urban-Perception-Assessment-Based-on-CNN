package com.yaindream.tracevideo;

import android.Manifest;
import android.annotation.SuppressLint;
import android.annotation.TargetApi;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.hardware.Camera;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.media.CamcorderProfile;
import android.media.MediaRecorder;
import android.os.Build;
import android.os.Environment;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.provider.Settings;
import android.util.Log;
import android.view.Surface;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;


public class MainActivity extends AppCompatActivity {

    private static final String TAG = "iLoveZheng";
    private Camera mCamera;
    private CameraPreview mPreview;
    private MediaRecorder mMediaRecorder;
    private boolean isRecording = false;

    public static final int MEDIA_TYPE_IMAGE = 1;
    public static final int MEDIA_TYPE_VIDEO = 2;
    private int mId;
    private String mPath;

    private LocationManager lm;
    private TextView tv_show;

    private String startTime;
    private String endTime;

    private StringBuilder locationInfo = new StringBuilder();
    private static File mediaStorageDir = null;
    private static String timeStamp;


    @RequiresApi(api = Build.VERSION_CODES.M)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        locationInfo.append("Time,Latitude,Longitude,Altitude,Speed,Bearing,Accuracy\n");

        mediaStorageDir = new File(Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_PICTURES), "MyCameraApp");
        if (! mediaStorageDir.exists()){
            if (! mediaStorageDir.mkdirs()){
                Log.d("MyCameraApp", "failed to create directory");
                return;
            }
        }

        // 开启位置服务
        tv_show = findViewById(R.id.tv_show);
        lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);

        if (!isGpsAble(lm)) {
            Toast.makeText(MainActivity.this, "请打开GPS~", Toast.LENGTH_SHORT).show();
            openGPS2();
        }

        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            return;
        }
        Location lc = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
        updateShow(lc);
        //设置间隔1秒获得一次GPS定位信息
        lm.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1000, 4, new LocationListener() {
            @Override
            public void onLocationChanged(Location location) {
                // 当GPS定位信息发生改变时，更新定位
                updateShow(location);
            }
            @Override
            public void onStatusChanged(String provider, int status, Bundle extras) {

            }
            @SuppressLint("MissingPermission")
            @Override
            public void onProviderEnabled(String provider) {
                updateShow(lm.getLastKnownLocation(provider));
            }
            @Override
            public void onProviderDisabled(String provider) {
                updateShow(null);
            }
        });

        Button captureButton = (Button) findViewById(R.id.button_capture);
        captureButton.setOnClickListener((View v) -> {
            if (isRecording) {
                endTime = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss:SSS").format(new Date());
                // stop recording and release camera
                mMediaRecorder.stop();  // stop the recording
                releaseMediaRecorder(); // release the MediaRecorder object
                mCamera.lock();         // take camera access back from MediaRecorder

                // inform the user that recording has stopped
                ((Button)v).setText("Capture");
                isRecording = false;
                // 把数据写入文件中
                writeLocationInfo();
            } else {
                // initialize video camera
                timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
                if (prepareVideoRecorder(mCamera)) {
                    // Camera is available and unlocked, MediaRecorder is prepared,
                    // now you can start recording
                    mMediaRecorder.start();
                    startTime = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss:SSS").format(new Date());

                    // inform the user that recording has started
                    ((Button)v).setText("Stop");
                    Toast.makeText(MainActivity.this, "录制文件保存在:"+mPath, Toast.LENGTH_LONG).show();
                    isRecording = true;
                } else {
                    // prepare didn't work, release the camera
                    releaseMediaRecorder();
                    // inform user
                }
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (mCamera != null) {
            mCamera.release();
            mCamera = null;
        }
        mId = FindBackCamera();
        System.out.println("mId = " + mId);
        try {
            mCamera = Camera.open(mId);
        } catch (Exception e) {
            Toast.makeText(MainActivity.this, "摄像头正在使用", Toast.LENGTH_LONG).show();
            return;
        }
//        mCamera.setFaceDetectionListener(new MyFaceDetectionListener());
        mPreview = new CameraPreview(MainActivity.this, mCamera, mId);
        FrameLayout preview = findViewById(R.id.camera_preview);
        preview.addView(mPreview);
    }

    // GPS是否可以使用
    private boolean isGpsAble(LocationManager lm){
        return lm.isProviderEnabled(LocationManager.GPS_PROVIDER);
    }

    // 打开设置页面让用户自己设置
    private void openGPS2() {
        Intent intent = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);
        startActivityForResult(intent, 0);
    }

    // 定义一个更新显示的方法
    private void updateShow(Location location) {
        if (location != null) {
            if (isRecording) {
                locationInfo.append(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss:SSS").format(new Date())).append(",");
                locationInfo.append(location.getLatitude()).append(",");
                locationInfo.append(location.getLongitude()).append(",");
                locationInfo.append(location.getAltitude()).append(",");
                locationInfo.append(location.getSpeed()).append(",");
                locationInfo.append(location.getBearing()).append(",");
                locationInfo.append(location.getAccuracy()).append("\n");
            }
            String sb = "当前的位置信息：\n" +
                    "经度：" + location.getLongitude() + "\n" +
                    "纬度：" + location.getLatitude() + "\n" +
                    "高度：" + location.getAltitude() + "\n" +
                    "速度：" + location.getSpeed() + "\n" +
                    "方向：" + location.getBearing() + "\n" +
                    "定位精度：" + location.getAccuracy() + "\n";
            tv_show.setText(sb);
        } else tv_show.setText("当前暂无GPS信号~~");
    }

    @TargetApi(9)
    private int FindBackCamera(){
        int cameraCount = 0;
        Camera.CameraInfo cameraInfo = new Camera.CameraInfo();
        cameraCount = Camera.getNumberOfCameras(); // get cameras number
        System.out.println("cameraCount = " + cameraCount);
        for ( int camIdx = 0; camIdx < cameraCount;camIdx++ ) {
            Camera.getCameraInfo( camIdx, cameraInfo ); // get camerainfo
            if ( cameraInfo.facing ==Camera.CameraInfo.CAMERA_FACING_BACK) {
                // 代表摄像头的方位，目前有定义值两个分别为CAMERA_FACING_FRONT前置和CAMERA_FACING_BACK后置
                return camIdx;
            }
        }
        return -1;
    }


    @Override
    protected void onPause() {
        super.onPause();
        releaseMediaRecorder();       // if you are using MediaRecorder, release it first
        releaseCamera();              // release the camera immediately on pause event
    }

    private void releaseMediaRecorder(){
        if (mMediaRecorder != null) {
            mMediaRecorder.reset();   // clear recorder configuration
            mMediaRecorder.release(); // release the recorder object
            mMediaRecorder = null;
            mCamera.lock();           // lock camera for later use
        }
    }

    private void releaseCamera(){
        if (mCamera != null){
            mCamera.release();        // release the camera for other applications
            mCamera = null;
        }
    }

    private boolean prepareVideoRecorder(Camera mCamera){

        mMediaRecorder = new MediaRecorder();
        // Step 1: Unlock and set camera to MediaRecorder
        mCamera.unlock();
        mMediaRecorder.setCamera(mCamera);

        // Step 2: Set sources
        mMediaRecorder.setAudioSource(MediaRecorder.AudioSource.CAMCORDER);
        mMediaRecorder.setVideoSource(MediaRecorder.VideoSource.CAMERA);

        // Step 3: Set a CamcorderProfile (requires API Level 8 or higher)
        mMediaRecorder.setProfile(CamcorderProfile.get(mId, CamcorderProfile.QUALITY_480P));

        // Step 4: Set output file
        mPath = getOutputMediaFile(MEDIA_TYPE_VIDEO).toString();
        System.out.println("path = " + mPath);
        mMediaRecorder.setOutputFile(mPath);

        // Step 5: Set the preview output
        Surface surface = mPreview.getHolder().getSurface();
        mMediaRecorder.setPreviewDisplay(surface);

        // Step 6: Prepare configured MediaRecorder
        try {
            mMediaRecorder.prepare();
        } catch (IllegalStateException e) {
            Log.d(TAG, "IllegalStateException preparing MediaRecorder: " + e.getMessage());
            releaseMediaRecorder();
            return false;
        } catch (IOException e) {
            Log.d(TAG, "IOException preparing MediaRecorder: " + e.getMessage());
            releaseMediaRecorder();
            return false;
        }
        return true;
    }

    private void writeLocationInfo() {
        RandomAccessFile raf = null;
        try {
            File csvFile = new File(mediaStorageDir.getPath() + File.separator +
                    "VID_"+ timeStamp + ".csv");
            raf = new RandomAccessFile(csvFile, "rwd");
            raf.write(locationInfo.toString().getBytes());
            raf.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

        String timeInfo = startTime + "\n" + endTime;
        try {
            File txtFile = new File(mediaStorageDir.getPath() + File.separator +
                    "VID_"+ timeStamp + ".txt");
            raf = new RandomAccessFile(txtFile, "rwd");
            raf.write(timeInfo.getBytes());
            raf.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    /** Create a File for saving an image or video */
    private static File getOutputMediaFile(int type){
        File mediaFile;
        if (type == MEDIA_TYPE_IMAGE){
            mediaFile = new File(mediaStorageDir.getPath() + File.separator +
                    "IMG_"+ timeStamp + ".jpg");
        } else if(type == MEDIA_TYPE_VIDEO) {
            mediaFile = new File(mediaStorageDir.getPath() + File.separator +
                    "VID_"+ timeStamp + ".mp4");
        } else {
            return null;
        }
        return mediaFile;
    }

    public class CameraPreview extends SurfaceView implements SurfaceHolder.Callback {
        private SurfaceHolder mHolder;
        private Camera mCamera;
        private int mId;

        public CameraPreview(Context context, Camera camera, int id) {
            super(context);
            mCamera = camera;
            mId = id;

            // Install a SurfaceHolder.Callback so we get notified when the
            // underlying surface is created and destroyed.
            mHolder = getHolder();
            mHolder.addCallback(this);
            // deprecated setting, but required on Android versions prior to 3.0
            mHolder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);
        }

        public void surfaceCreated(SurfaceHolder holder) {
            // The Surface has been created, now tell the mCamera where to draw the preview.
            try {
                mCamera.setPreviewDisplay(holder);
                mCamera.startPreview();
            } catch (IOException e) {
                Log.d(TAG, "Error setting mCamera preview: " + e.getMessage());
            }
        }

        public void surfaceDestroyed(SurfaceHolder holder) {
            // empty. Take care of releasing the Camera preview in your activity.
            // Surface will be destroyed when we return, so stop the preview.
            if (mCamera != null) {
                // Call stopPreview() to stop updating the preview surface.
                mCamera.stopPreview();
            }
        }

        public void surfaceChanged(SurfaceHolder holder, int format, int w, int h) {

            // If your preview can change or rotate, take care of those events here.
            // Make sure to stop the preview before resizing or reformatting it.

            if (mHolder.getSurface() == null){// preview surface does not exist
                return;
            }

            // stop preview before making changes
            try {
                mCamera.stopPreview();
            } catch (Exception e){
                // ignore: tried to stop a non-existent preview
            }

            // set preview size and make any resize, rotate or reformatting changes here
            setCameraDisplayOrientation(MainActivity.this, mId, mCamera);
            List<Camera.Size> supportedPreviewSizes = mCamera.getParameters().getSupportedPreviewSizes();
            for (Camera.Size size : supportedPreviewSizes) {
                System.out.println("Width = " + size.width + "  Height = " + size.height);
            }
            Camera.Parameters parameters = mCamera.getParameters();

            parameters.setPreviewSize(1920, 1080);
            mCamera.setParameters(parameters);
            // start preview with new settings
            try {
                mCamera.setPreviewDisplay(mHolder);
                mCamera.startPreview();
                mCamera.cancelAutoFocus();// 2如果要实现连续的自动对焦，这一句必须加上
                // 设置自动对焦
                mCamera.autoFocus((success, camera) -> {
                    if (success) {
                        camera.cancelAutoFocus();//只有加上了这一句，才会自动对焦。
                    }
                });
            } catch (Exception e){
                Log.d(TAG, "Error starting mCamera preview: " + e.getMessage());
            }
        }

        public void setCameraDisplayOrientation(AppCompatActivity activity,
                                                int cameraId, android.hardware.Camera camera) {
            android.hardware.Camera.CameraInfo info =
                    new android.hardware.Camera.CameraInfo();
            android.hardware.Camera.getCameraInfo(cameraId, info);
            int rotation = activity.getWindowManager().getDefaultDisplay()
                    .getRotation();
            int degrees = 0;
            switch (rotation) {
                case Surface.ROTATION_0: degrees = 0; break;
                case Surface.ROTATION_90: degrees = 90; break;
                case Surface.ROTATION_180: degrees = 180; break;
                case Surface.ROTATION_270: degrees = 270; break;
            }

            int result;
            if (info.facing == Camera.CameraInfo.CAMERA_FACING_FRONT) {
                result = (info.orientation + degrees) % 360;
                result = (360 - result) % 360;  // compensate the mirror
            } else {  // back-facing
                result = (info.orientation - degrees + 360) % 360;
            }
            camera.setDisplayOrientation(result);
        }
    }
}
