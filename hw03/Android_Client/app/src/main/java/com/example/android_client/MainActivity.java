package com.example.android_client;

import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;
import java.net.InetSocketAddress;

import androidx.appcompat.app.AppCompatActivity;


public class MainActivity extends AppCompatActivity {
    public EditText ip, port, text;
    public TextView chattings, chat, chat2;
    public DataInputStream dataInputStream;
    public DataOutputStream dataOutputStream;
    public String readtext, writetext, recv, send;

    @Override
    protected void onCreate(Bundle savedInstanceState) { // onCreate
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // findViewById 사용
        ip = (EditText) findViewById(R.id.ip);
        port = (EditText) findViewById(R.id.port);
        text = (EditText) findViewById(R.id.msg);
        chattings = (TextView) findViewById(R.id.chattings);
    }

    public void execServer(View view) { // 서버와 연결
        new Thread() { // 쓰레드
            public void run() { // run
                try {
                    Socket socket = new Socket(); // 소켓 생성
                    while (true) {
                        socket.connect(new InetSocketAddress(ip.getText().toString(), Integer.parseInt(port.getText().toString()))); // connect
                        dataInputStream = new DataInputStream(socket.getInputStream()); // 데이터 입력
                        dataOutputStream = new DataOutputStream(socket.getOutputStream()); // 데이터 출력
                        recvClient();
                    }
                } catch (IOException e) { // exception
                    e.printStackTrace();
                }
            }
        }.start(); // 쓰레드 실행
    }

    public void recvClient() { // 서버로부터 text를 받음
        new Thread() { // 쓰레드
            public void run() { // run
                try {
                    while (true) {
                        readtext = dataInputStream.readUTF();
                        runOnUiThread(new Runnable() { // runOnUiThread
                            public void run() { // run
                                chat = (TextView) findViewById(R.id.chattings); // chat findViewById
                                recv = "[RECV]"; // 수신완료를 출력하기 위해 생성
                                readtext = recv.concat(readtext); // concat
                                chat.setText(readtext); // setText
                            }
                        });
                    }
                } catch (IOException e) { // exception
                    e.printStackTrace();
                }
            }
        }.start(); // 쓰레드 실행
    }

    public void SendServer(View view) { // 서버로 text를 보냄
        new Thread() { // 쓰레드
            public void run() { // run
                try {
                    writetext = text.getText().toString();
                    dataOutputStream.writeUTF(writetext);
                    runOnUiThread(new Runnable() {
                        public void run() { // run
                            chat2 = (TextView) findViewById(R.id.chattings); // chat2 findViewById
                            send = "[SEND]"; // 송신완료를 출력하기 위해 생성
                            writetext = send.concat(writetext); // concat
                            chat2.setText(writetext); // setText
                        }
                    });
                } catch (IOException e) { // exception
                    e.printStackTrace();
                }
            }
        }.start(); // 쓰레드 실행
    }
}