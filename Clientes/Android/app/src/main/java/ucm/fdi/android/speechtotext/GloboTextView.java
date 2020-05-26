/*
 * GloboTextView.java
 * Created by Jose Luis Moreno on 26/05/20 16:40
 * MIT License
 * Copyright (c) 2020 . Mauricio Abbati Loureiro - Jose Luis Moreno Varillas
 * Last modified 26/05/20 16:40
 */

package ucm.fdi.android.speechtotext;



import android.content.Context;
import android.graphics.Color;
import android.util.AttributeSet;
import android.support.v7.widget.AppCompatTextView;

public class GloboTextView extends AppCompatTextView  {

    public GloboTextView(Context context) {
        super(context);
        init(true, context);
    }

    public GloboTextView(Context context, boolean incoming) {
        super(context);
        init(incoming, context);
    }

    public GloboTextView(Context context, AttributeSet attrs) {
        super(context, attrs);
        init(true, context);
    }

    public GloboTextView(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init(true, context);
    }


    private void init(boolean incoming, Context context){
        setText("Hello World");
        setIncoming(incoming, context);

        final float dpscale = context.getResources().getDisplayMetrics().density;
        this.setLineSpacing((int) (2 * dpscale + 0.5f), 1.0f);
    }

    public void setIncoming(boolean incoming, Context context)
    {
        final float dpscale = context.getResources().getDisplayMetrics().density;
        if (incoming) {
            this.setBackgroundResource(R.drawable.shape_bg_incomming_bubble);
            this.setTextColor(Color.WHITE);
            this.setPadding((int) (20 * dpscale + 0.5f),
                    (int) (4 * dpscale + 0.5f),
                    (int) (10 * dpscale + 0.5f),
                    (int) (10 * dpscale + 0.5f));
        }
        else {
            this.setPadding((int) (10 * dpscale + 0.5f),
                    (int) (4 * dpscale + 0.5f),
                    (int) (20 * dpscale + 0.5f),
                    (int) (10 * dpscale + 0.5f));
            this.setTextColor(Color.BLACK);
            this.setBackgroundResource(R.drawable.shape_bg_outgoing_bubble);
        }
    }
}