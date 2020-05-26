
/*
 * MainActivity.java
 * Created by Jose Luis Moreno on 5/11/19 9:49 PM
 * MIT License
 * Copyright (c) 2019 . Mauricio Abbati Loureiro - Jose Luis Moreno Varillas
 * Last modified 5/5/19 1:16 PM
 */

package ucm.fdi.android.speechtotext;

import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.speech.RecognizerIntent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Html;
import android.text.util.Linkify;
import android.view.Gravity;
import android.view.View;

import java.io.InputStream;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;

import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.LinearLayout.LayoutParams;
import android.speech.tts.TextToSpeech;
import android.widget.ProgressBar;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.concurrent.ExecutionException;

import ucm.fdi.android.speechtotext.Items.Book;
import ucm.fdi.android.speechtotext.Items.Location;
import ucm.fdi.android.speechtotext.Items.Phone;
import ucm.fdi.android.speechtotext.Items.Email;

public class MainActivity extends AppCompatActivity {

    private static final int REQ_CODE_SPEECH_INPUT = 100;
    private static TextToSpeech t;
    private ImageButton mSpeakBtn;
    private Button mSendBtn;
    private TextView textField;
    private ProgressBar progressBar;
    private Locale locSpanish = new Locale("es", "ES");
    private SendAndReceiveTask mTask = null;
    private String user_id;

    private String coverPattern = "http://covers.openlibrary.org/b/isbn/%s-M.jpg?default=false";

    private static JSONObject resultado;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mSpeakBtn = (ImageButton) findViewById(R.id.btnSpeak);
        t = new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status != TextToSpeech.ERROR){
                    t.setLanguage(locSpanish);
                }
            }
        });
        mSendBtn = (Button) findViewById(R.id.enviar);
        mSendBtn.setOnClickListener(new View.OnClickListener(){
            public void onClick (View v){
                startVoiceInput();
            }
        });

        textField = (TextView) findViewById(R.id.textField);
        progressBar = (ProgressBar) findViewById(R.id.progressBar);
        progressBar.setVisibility(View.INVISIBLE);

        mSendBtn.setOnClickListener(new View.OnClickListener(){
            public void onClick (View v){
                sendTextInput();
            }
        });
        SharedPreferences sp = this.getSharedPreferences("user_id", MODE_PRIVATE);
        user_id = sp.getString("user_id",null);
    }

    private void start(){
        String result = "busca un libro llamado Harry Potter";
        newSimpleEntryText(result, true);
        mTask = new SendAndReceiveTask(result, this);
        setSpinnerVisibility(true);
        mTask.execute();
    }

    private void startVoiceInput() {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
        try {
            startActivityForResult(intent, REQ_CODE_SPEECH_INPUT);
        } catch (ActivityNotFoundException a) {

        }

        ScrollView scrollView = (ScrollView) findViewById(R.id.scroll);
        scrollView.fullScroll(View.FOCUS_DOWN);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        switch (requestCode) {
            case REQ_CODE_SPEECH_INPUT: {
                if (resultCode == RESULT_OK && null != data) {
                    ArrayList<String> result = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                    newSimpleEntryText(result.get(0), true);
                    mTask = new SendAndReceiveTask(result.get(0), this);
                    setSpinnerVisibility(true);
                    mTask.execute();
                }
                break;
            }
        }
    }

    private void formatResponse(JSONObject resultado) throws JSONException {
        if(resultado.get("errorno").toString().equals("0"))
            newObjectEntry(resultado);
    }

    private void newObjectEntry(JSONObject resultado) {
        try {
            LinearLayout linearLayout = (LinearLayout) findViewById(R.id.conversationContainer);
            GloboTextView mResponse = new GloboTextView(this, true);
            GloboTextView mInfo = new GloboTextView(this, true);
            ImageView mCover = new ImageView(this);

            LayoutParams layoutParams = new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT);
            layoutParams.gravity = Gravity.LEFT;
            layoutParams.setMargins(0, 0, 0, 40);

            mCover.setLayoutParams(layoutParams);
            mResponse.setLayoutParams(layoutParams);
            mInfo.setLayoutParams(layoutParams);

            switch(resultado.get("content-type").toString()) {
                case "list-books":
                    JSONArray books = resultado.getJSONArray("books");
                    ArrayList<Book> infoBooks = processBooks(books,mCover);
                    newSimpleEntryText(resultado.get("response").toString(),false);
                    for(Book book:infoBooks)
                        linearLayout.addView(setInfoBookView(book));
                    break;
                case "single-book":
                    Book book = processBook(resultado);
                    newSimpleEntryText(resultado.get("response").toString(),false);
                    linearLayout.addView(setInfoBookView(book));
                    break;
                case "location":
                    Location loc = processLocation(resultado);
                    newSimpleEntryText(resultado.get("response").toString(),false);
                    linearLayout.addView(newLocationEntry(loc));
                    break;
                case "phone":
                    Phone phone = processPhone(resultado);
                    newSimpleEntryText(resultado.get("response").toString(),false);
                    linearLayout.addView(newPhoneEntry(phone));
                    break;
                case "email":
                    Email email = processEmail(resultado);
                    newSimpleEntryText(resultado.get("response").toString(),false);
                    linearLayout.addView(newEmailEntry(email));
                    break;
                default:
                    newSimpleEntryText(resultado.get("response").toString(),false);
                    break;
            }
        } catch (JSONException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
    }

    private ArrayList<Book> processBooks(JSONArray books, ImageView mCover) throws JSONException, ExecutionException, InterruptedException {
        ArrayList<Book> infoBooks = new ArrayList<>();
        JSONObject bookJSON = null;

        for (int i = 0; i < books.length(); ++i) {
            bookJSON = books.getJSONObject(i);

            String title = bookJSON.get("title").toString();
            String author = bookJSON.get("author").toString();

            ArrayList<String> isbnList = new ArrayList<>();
            JSONArray isbnsJSON = bookJSON.getJSONArray("isbn");
            for(int j = 0; j < isbnsJSON.length();++j)
                isbnList.add(isbnsJSON.get(j).toString());

            Book infoBook = new Book(title, author,isbnList);

            infoBooks.add(infoBook);
        }
        return infoBooks;
    }

    private Book processBook(JSONObject resultado) throws JSONException {
        String title = resultado.get("title").toString();
        String author = resultado.get("author").toString();

        String available = "";

        JSONArray availableJSONArray = resultado.getJSONArray("available");
        String availableRaw = availableJSONArray.get(0).toString();
        availableRaw = availableRaw.substring(1,availableRaw.length()-1);
        if(availableRaw.length() > 0) {
            List<String> availableListRaw = Arrays.asList(availableRaw.split(","));
            for (String availableUnitRaw : availableListRaw) {
                String[] aux = availableUnitRaw.split(":");
                available += aux[0].substring(1, aux[0].length() - 1) + "\t:\t" + aux[1] + "<br>";
            }
        }
        else
            available = "No disponible";

        ArrayList<String> isbnList = new ArrayList<>();
        JSONArray isbnsJSON = resultado.getJSONArray("isbn");
        for(int j = 0; j < isbnsJSON.length();++j)
            isbnList.add(isbnsJSON.get(j).toString());

        String url = resultado.get("url").toString();


        return new Book(title,author,isbnList,available, url);
    }

    private LinearLayout setInfoBookView(Book book){

        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.HORIZONTAL);
        LayoutParams params = new LayoutParams(LayoutParams.WRAP_CONTENT,LayoutParams.WRAP_CONTENT);
        params.setMargins(0, 0, 0, 40);
        int coverWidth = 210;
        int coverHeight = 280;
        LayoutParams paramsCover = new LayoutParams(coverWidth,coverHeight);

        GloboTextView text = new GloboTextView(this, true);
        ImageView image = new ImageView(this);

        boolean success = false;
        ArrayList<String> isbnList = book.getISBNList();
        for(int i = 0; i < isbnList.size() && !success;++i) {
            String url = String.format(coverPattern,isbnList.get(i));
            try {
                Bitmap bmp = new DownloadImageTaskToImageView().execute(url).get();
                if(null != bmp) {
                    success = true;
                    image.setImageBitmap(bmp);
                }
            } catch (ExecutionException e) {
                e.printStackTrace();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        if(null == image.getDrawable())
            Picasso.get().load(R.drawable.empty_book).fit().into(image);

        image.setPadding(0,0,15,0);
        image.setLayoutParams(paramsCover);


        if(book.getUrl().length() > 0){
            final String url = book.getUrl();
            image.setOnClickListener(new View.OnClickListener() {
                public void onClick(View v)
                {

                    Uri uri = Uri.parse(url);
                    Intent intent = new Intent(Intent.ACTION_VIEW, uri);
                    startActivity(intent);
                }
            });
        }


        layout.addView(image);

        String info = "<b> " + book.getTitle() + "</b><br><br>"  + book.getAuthor() + "<br><br>" +book.getAvailable();
        text.setText(Html.fromHtml(info));

        text.setLayoutParams(params);
        layout.addView(text);

        layout.setLayoutParams(params);

        return layout;

    }

    private Phone processPhone(JSONObject phoneJSON)throws JSONException{
        String phone = phoneJSON.get("phone").toString();
        String library = phoneJSON.get("library").toString();

        return new Phone(phone,library);
    }

    private Email processEmail(JSONObject emailJSON)throws JSONException{
        System.out.println(emailJSON);
        String email = emailJSON.get("email").toString();
        String library = emailJSON.get("library").toString();

        return new Email(email,library);
    }

    private Location processLocation(JSONObject locationJSON) throws JSONException{
        String library = locationJSON.get("library").toString();
        String location = locationJSON.get("location").toString();
        String latitud = locationJSON.get("lat").toString();
        String longitud = locationJSON.get("long").toString();

        return new Location(library,location,latitud,longitud);
    }

    private void newSimpleEntryText(String message, boolean isUser) {

        LinearLayout linearLayout = (LinearLayout) findViewById(R.id.conversationContainer);
        GloboTextView mTextViewMessage = new GloboTextView(this, !isUser);
        LayoutParams layoutParams = new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT);
        layoutParams.setMargins(0, 0, 0, 40);

        if (!isUser){
            layoutParams.gravity = Gravity.LEFT;
            t.speak(message, TextToSpeech.QUEUE_FLUSH, null, null);

        }else{
            layoutParams.gravity = Gravity.RIGHT;
            mTextViewMessage.setIncoming(!isUser, this);
        }
        mTextViewMessage.setLayoutParams(layoutParams);
        mTextViewMessage.setText(message);
        linearLayout.addView(mTextViewMessage);
    }

    private LinearLayout newLocationEntry(final Location location) throws ExecutionException, InterruptedException {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        LayoutParams params = new LayoutParams(LayoutParams.WRAP_CONTENT,LayoutParams.WRAP_CONTENT);
        params.setMargins(0, 0, 0, 40);


        GloboTextView libraryTextView = new GloboTextView(this, true);
        ImageView mapImageView = new ImageView(this);
        TextView locationTextView = new GloboTextView(this, true);

        libraryTextView.setText(Html.fromHtml("<b>"+location.getLibrary()+"<b>"));
        layout.addView(libraryTextView);

        String urlBase ="https://maps.googleapis.com/maps/api/staticmap?";

        String apiKey = "AIzaSyAQCrR8SxPRznlDMyLgxoK1iuCAdXAOBz0";

        String atributtes = "center=" + location.getLatitud() + "," + location.getLongitud() + "&zoom=16&size=750x450&markers=color:blue%7C"+location.getLatitud()+","+location.getLongitud()+"&key="+apiKey;

        String url = urlBase + atributtes;
        Bitmap map = new DownloadImageTaskToImageView().execute(url).get();
        mapImageView.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                onClickMapImage(location);
            }
        });

        mapImageView.setImageBitmap(map);
        layout.addView(mapImageView);

        locationTextView.setText(location.getLocation());
        layout.addView(locationTextView);

        layout.setLayoutParams(params);

        return layout;
    }

    private void onClickMapImage(Location location){
        Uri gmmIntentUri = Uri.parse("geo:<"+ location.getLatitud()+ ">,<"+location.getLongitud()+">?q=<"+location.getLatitud()+ ">,<"+location.getLongitud()+">("+location.getLibrary()+")");
        Intent mapIntent = new Intent(Intent.ACTION_VIEW, gmmIntentUri);
        mapIntent.setPackage("com.google.android.apps.maps");
        if (mapIntent.resolveActivity(getPackageManager()) != null) {
            startActivity(mapIntent);
        }
    }

    private LinearLayout newPhoneEntry(Phone phone){
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        LayoutParams params = new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT);
        params.setMargins(0, 0, 0, 40);

        GloboTextView libraryTextView = new GloboTextView(this, true);
        String libraryText = phone.getLibrary();
        libraryTextView.setText(Html.fromHtml("<b>"+libraryText+"</b>"));
        layout.addView(libraryTextView);

        GloboTextView phoneNumberTextView = new GloboTextView(this, true);
        phoneNumberTextView.setText(phone.getPhone());
        phoneNumberTextView.setTextSize(20);
        Linkify.addLinks(phoneNumberTextView, Linkify.ALL);
        layout.addView(phoneNumberTextView);

        layout.setLayoutParams(params);
        return layout;
    }

    private LinearLayout newEmailEntry(Email email){
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        LayoutParams params = new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT);
        params.setMargins(0, 0, 0, 40);


        GloboTextView libraryTextView = new GloboTextView(this, true);
        String libraryText = email.getLibrary();
        libraryTextView.setText(Html.fromHtml("<b>"+libraryText+"</b>"));
        layout.addView(libraryTextView);

        GloboTextView emailTextView = new GloboTextView(this, true);
        emailTextView.setText(email.getEmail());
        emailTextView.setTextSize(20);
        Linkify.addLinks(emailTextView, Linkify.ALL);
        layout.addView(emailTextView);

        layout.setLayoutParams(params);
        return layout;
    }

    public void sendTextInput() {
        String text = textField.getText().toString();
        if (!text.equals("")){
            textField.setText("");
            newSimpleEntryText(text, true);
            mTask = new SendAndReceiveTask(text, this);
            setSpinnerVisibility(true);
            mTask.execute();
        }
    }

    public void setSpinnerVisibility(boolean visible)
    {
        mSendBtn.animate().alpha(visible ? 0.0f : 1.0f).setDuration(500);
        textField.animate().alpha(visible ? 0.0f : 1.0f).setDuration(500);
        mSpeakBtn.animate().alpha(visible ? 0.0f : 1.0f).setDuration(500);
        progressBar.animate().alpha(visible ? 1.0f : 0.0f).setDuration(350);


        mSendBtn.setVisibility(visible ? View.INVISIBLE : View.VISIBLE);
        textField.setVisibility(visible ? View.INVISIBLE : View.VISIBLE);
        mSpeakBtn.setVisibility(visible ? View.INVISIBLE : View.VISIBLE);
        progressBar.setVisibility(visible ? View.VISIBLE : View.INVISIBLE);
        mSendBtn.setEnabled(!visible);
        textField.setEnabled(!visible);
        mSpeakBtn.setEnabled(!visible);
    }

    private class SendAndReceiveTask extends AsyncTask<Void, Void, Boolean>{

        private final String message;
        private final Context ctx;

        SendAndReceiveTask(String _message, Context _ctx){
            message = _message;
            ctx = _ctx;
        }

        @Override
        protected Boolean doInBackground(Void... voids) {
            //En esta funcion se envian los datos al servidor y se deshabilita el boton



            Connection conn = new Connection();
            String type = "query";

            String query = null;
            if(null == user_id || user_id.length() <= 0)
                query ="content=" + message;
            else
                query = "user_id="+user_id+"&content=" + message;
            resultado = conn.ejecutar( "type="+type,query);
            //TODO: mostrar errores en toast
            try {
                String aux = resultado.get("errorno").toString();
                if(!resultado.get("errorno").toString().equals("0")){
                    return false;
                }
            } catch (JSONException e) {
                e.printStackTrace();
                return false;
            }

            return true;
        }

        @Override
        protected void onPostExecute(final Boolean success) {
            if(!success){
                try {
                    Toast.makeText(ctx,resultado.get("errorMessage").toString() ,Toast.LENGTH_LONG).show();
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }else {
                try {
                    if (null == user_id || user_id.length() <= 0) {
                        SharedPreferences sp = getSharedPreferences("user_id", 0);
                        SharedPreferences.Editor Ed = sp.edit();
                        Ed.putString("user_id", resultado.get("user_id").toString());
                        Ed.apply();
                        Ed.commit();
                    }
                    formatResponse(resultado);
                    ScrollView scrollView = (ScrollView) findViewById(R.id.scroll);
                    scrollView.fullScroll(View.FOCUS_DOWN);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
            setSpinnerVisibility(false);
        }

    }

    public class DownloadImageTaskToImageView extends AsyncTask<String, Void, Bitmap> {

        public DownloadImageTaskToImageView(){}

        protected Bitmap doInBackground(String... urls) {
            String urldisplay = urls[0];
            Bitmap mIcon11 = null;
            try {
                InputStream in = new java.net.URL(urldisplay).openStream();
                mIcon11 = BitmapFactory.decodeStream(in);
                if(mIcon11.getHeight() <=0)
                    mIcon11 = BitmapFactory.decodeResource(getResources(), R.drawable.empty_book);
            } catch (Exception e) {
                e.printStackTrace();
            }
            return mIcon11;
        }
    }
}
