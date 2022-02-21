package thedrake;

public class Offset2D {
    public final int x;
    public final int y;
    public Offset2D(int x, int y) {
        this.x = x;
        this.y = y;
    }
    public boolean equalsTo(int x, int y)
    {
        if(x==this.x&&y==this.y)
            return true;
        return false;
    }
    public Offset2D yFlipped(){
        Offset2D test=new Offset2D( x, -y);
        return  test;
    }
}

