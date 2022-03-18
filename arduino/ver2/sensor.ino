unsigned long ibi;
unsigned long t0;
unsigned long t;
bool first=true;

const int max_heartpluse_duty = 2000;//you can change it follow your system's request.
                        //2000 meams 2 seconds. System return error 
                        //if the duty overtrip 2 second.
void setup()
{
    Serial.begin(9600);
    attachInterrupt(0, interrupt, RISING);//set interrupt 0,digital port 2
}
void loop()
{
}

/*Function: Interrupt service routine.Get the sigal from the external interrupt*/
void interrupt()
{
    t = millis();
    if(first)
    {
      t0 = t;
      first = false;
    }
    else
    {
      ibi = t - t0;
      t0 = t;
      if (ibi < max_heartpluse_duty)
      {
        Serial.println(ibi);
      }
      else
      {
        first = true;
      }
    }
}