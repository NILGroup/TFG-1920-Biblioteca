/*
 * GloboTextView.java
 * Created by Jose Luis Moreno on 26/05/20 16:40
 * MIT License
 * Copyright (c) 2020 . Mauricio Abbati Loureiro - Jose Luis Moreno Varillas
 * Last modified 26/05/20 16:40
 */

package es.ucm.fdi.janet;



import android.content.Context;
import android.graphics.Color;
import android.util.AttributeSet;
import android.support.v7.widget.AppCompatTextView;

public class GloboTextView extends AppCompatTextView  {

    private boolean incoming;

    public GloboTextView(Context context) {
        super(context);
        init(true, context, false);
    }

    public GloboTextView(Context context, boolean incoming, boolean high_contrast) {
        super(context);
        init(incoming, context, high_contrast);
    }

    public GloboTextView(Context context, AttributeSet attrs) {
        super(context, attrs);
        init(true, context, false);
    }

    public GloboTextView(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init(true, context, false);
    }


    private void init(boolean incoming, Context context, boolean high_contrast){
        this.incoming = incoming;
        setIncoming(context, high_contrast);

        final float dpscale = context.getResources().getDisplayMetrics().density;
        this.setLineSpacing((int) (2 * dpscale + 0.5f), 1.0f);
    }

    public void setIncoming(Context context, boolean high_contrast)
    {
        final float dpscale = context.getResources().getDisplayMetrics().density;
        if (incoming) {
            if (high_contrast)
                this.setBackgroundResource(R.drawable.shape_bg_incomming_bubble_contrast);
            else
                this.setBackgroundResource(R.drawable.shape_bg_incomming_bubble);
            this.setTextColor(Color.WHITE);
            this.setPadding((int) (20 * dpscale + 0.5f),
                    (int) (4 * dpscale + 0.5f),
                    (int) (10 * dpscale + 0.5f),
                    (int) (10 * dpscale + 0.5f));
        }
        else {
            if (high_contrast) {
                this.setBackgroundResource(R.drawable.shape_bg_outgoing_bubble_contrast);
                this.setTextColor(Color.WHITE);
            }
            else {
                this.setBackgroundResource(R.drawable.shape_bg_outgoing_bubble);
                this.setTextColor(Color.BLACK);
            }
            this.setPadding((int) (10 * dpscale + 0.5f),
                    (int) (4 * dpscale + 0.5f),
                    (int) (20 * dpscale + 0.5f),
                    (int) (10 * dpscale + 0.5f));

        }
    }
}