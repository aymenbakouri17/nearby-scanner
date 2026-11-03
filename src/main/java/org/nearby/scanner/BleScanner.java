
package org.nearby.scanner;

import android.annotation.SuppressLint;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.content.Context;
import android.os.Build;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.LinkedHashMap;
import java.util.Map;

public class BleScanner {

    private static BluetoothLeScanner scanner;
    private static ScanCallback callback;
    private static boolean scanning = false;

    private static final Map<String, JSONObject> devices =
            new LinkedHashMap<>();

    @SuppressLint("MissingPermission")
    public static synchronized void startScan(Context context) {

        if (scanning) return;

        try {
            BluetoothManager manager =
                    (BluetoothManager) context.getSystemService(
                            Context.BLUETOOTH_SERVICE);

            BluetoothAdapter adapter = manager.getAdapter();

            if (adapter == null || !adapter.isEnabled()) {
                return;
            }

            scanner = adapter.getBluetoothLeScanner();

            if (scanner == null) return;

            devices.clear();

            callback = new ScanCallback() {

                @Override
                public void onScanResult(int callbackType,
                                         ScanResult result) {

                    try {
                        String address =
                                result.getDevice().getAddress();

                        String name = null;

                        if (Build.VERSION.SDK_INT >= 26) {
                            name = result.getScanRecord() != null
                                    ? result.getScanRecord().getDeviceName()
                                    : null;
                        } else {
                            name = result.getDevice().getName();
                        }

                        JSONObject device = new JSONObject();

                        device.put("name",
                                name == null ? "Unknown" : name);

                        device.put("address", address);
                        device.put("rssi", result.getRssi());

                        synchronized (devices) {
                            devices.put(address, device);
                        }

                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            };

            scanner.startScan(callback);
            scanning = true;

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @SuppressLint("MissingPermission")
    public static synchronized void stopScan() {

        try {
            if (scanner != null && callback != null && scanning) {
                scanner.stopScan(callback);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        scanning = false;
    }

    public static String getResultsJson() {

        JSONArray array = new JSONArray();

        synchronized (devices) {
            for (JSONObject device : devices.values()) {
                array.put(device);
            }
        }

        return array.toString();
    }

    public static boolean isScanning() {
        return scanning;
    }
}
