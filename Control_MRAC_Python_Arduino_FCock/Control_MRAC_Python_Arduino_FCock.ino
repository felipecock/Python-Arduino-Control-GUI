#define IN 5
#include <math.h>
double SetPoint = 0; //Este es el punto de referencia del HMI (0.255).
double SystemOutput = 0; //Esta es la magnitud de la varible de control (0-1024).
byte toByte = 0; //Esta variable almacena el valor de la planta en un byte para luego enviarlo al HMI (00000000-11111111).
int R2 = 10000; //Este es el valor en Ohmios de la resistencia en el divisor de voltaje.

float Yk = 0;
float Mk = 0;
float Ek = 0;
float Uk = 0;
float Error = 0;
float Ym = 0;
double ControlSignal = 0; //Esta es la senal de control que le envía el arduino al sistema

//-------------------------------------CONTROL MRAC-------------------------------------------------------
  //Coeficientes de la función de transferencia
  float c0r=0,  c1r=0.21507,    c0c=1,  c1c=0; 
  // Límites del escalamiento / normalización
  float d1r=-1.43551,   d1c=-1; 
  float r, y, mr, mc, m, e, er, out_f;
  float p1r=0,p1c=0,p1_antr=0,p1_antc=0;
  int ci=0;
  
  float Kp=0.707;
  
  float MR_a[4]={0,0,0,0};
  float MR_b[4]={0,0,0,0};
  float MR_Pk[4]={0,0,0,0};
  float MR_Pk_1[4]={0,0,0,0};
  
  float Ctrl_a[3]={0,0,0};
  float Ctrl_b[3]={0,0,0};
  float Ctrl_Pk[3]={0,0,0};
  float Ctrl_Pk_1[3]={0,0,0};
  
  float Planta_a[3]={0,0,0};
  float Planta_b[3]={0,0,0};
  float Planta_Pk[3]={0,0,0};
  float Planta_Pk_1[3]={0,0,0};
  
//------------------------------------------------------------------------------------------------------

void setup(){
  Serial.begin(9600); //Se incia la comnicación por el puerto serial a una tasa de transferencia de 9600 baudios.
  pinMode(13, OUTPUT);
}

void loop(){
  if (Serial.available()>0){ //Cada que el Arduino recive un dato por el puerto serial, lee la variable de control y la envia al HMI.
    SetPoint = Serial.read();
    SetPoint /= 2.55;
    SystemOutput = analogRead(IN);
    SystemOutput = 1033209/pow(R2*(1024/(SystemOutput)-1),1.37265217541467); //Linealización del voltaje en Lux
    
    Controladp();
    
    if(ControlSignal > 255) ControlSignal=255;   //Saturación de la señal de control   
    if(ControlSignal < 0) ControlSignal=0;     //Saturación de la señal de control
    analogWrite(10, ControlSignal);
    Serial.print(SystemOutput,2);
    Serial.print(';');
    Serial.print(ControlSignal/2.55,2);
    Serial.print(';');
    Serial.print(Ym,2);
    Serial.print(';');
    Serial.println(Error,2);
  }
}

void Controladp() {
  ci=ci+1;
  r=SetPoint/100.0; //Se normaliza la señal de entrada
    
  y=(SystemOutput)/(100.0); //Intensidad de Luz normalizada 0.0-1.0
  
  //Controlador
  // Se ejecuta el modelo de referencia    
  mr=c0r*r+p1_antr;
  Ym = mr;
  p1r=c1r*r-d1r*mr;
  p1_antr=p1r;
  
  // Se calcula el error relativo  
  er=-1*(y-mr);
  
  // Se calcula el error que ingresa al controlador
  e=er*r;
  
  ModelReference(Uk);
  
  // Se ejecuta el controlador
  mc=c0c*e+p1_antc;
  p1c=c1c*e-d1c*mc;
  p1_antc=p1c;
  
  Planta(Controlador(Uk)); //Estimador de la respuesta del Sistema Controlador+Planta en Lazo Cerrado por medio de estructura 2D
  
  if (ci==1){
    mc=1;
  }
  
  // Se calcula la señal de control
  m=mc*r;
  ControlSignal=m;
}

float ModelReference(float Input){ //Estimador de la respuesta del modelo de referencia por medio de estructura 2D
   
   float Output = (MR_a[0]*Input) + MR_Pk_1[1];
   
   MR_Pk[1] = (MR_a[1]*Input) - (MR_b[1]*Output) + MR_Pk_1[2];
   MR_Pk[2] = (MR_a[2]*Input) - (MR_b[2]*Output) + MR_Pk_1[3];
   MR_Pk[3] = (MR_a[3]*Input) - (MR_b[3]*Output);
 
   MR_Pk_1[1] = MR_Pk[1];
   MR_Pk_1[2] = MR_Pk[2];
   MR_Pk_1[3] = MR_Pk[3];

   return(Output);
 }
 
 float Controlador(float Input){  //Estimador de la respuesta del controlador por medio de estructura 2D
   
   float Output = (Ctrl_a[0]*Input) + Ctrl_Pk_1[1];
   
   Ctrl_Pk[1] = (Ctrl_a[1]*Input) - (Ctrl_b[1]*Output) + Ctrl_Pk_1[2];
   Ctrl_Pk[2] = (Ctrl_a[2]*Input) - (Ctrl_b[2]*Output);
 
   Ctrl_Pk_1[1] = Ctrl_Pk[1];
   Ctrl_Pk_1[2] = Ctrl_Pk[2];
   
   return(Output);
 }
 
 float Planta(float Input){  //Estimador de la respuesta de la planta por medio de estructura 2D
   
   float Output = (Planta_a[0]*Input) + Planta_Pk_1[1];
   
   Planta_Pk[1] = (Planta_a[1]*Input) - (Planta_b[1]*Output) + Planta_Pk_1[2];
   Planta_Pk[2] = (Planta_a[2]*Input) - (Planta_b[2]*Output);
 
   Planta_Pk_1[1] = Planta_Pk[1];
   Planta_Pk_1[2] = Planta_Pk[2];
   
   return(Output);
 }
