public class MainActivity extends AppCompatActivity {

    private GpsTracker gpsTracker;
    private String x = "", y = "", address = "";
    
    private date = "", time = "";
 
  @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        gpsTracker = new GpsTracker(this);

        double latitude = gpsTracker.getLatitude();
        double longitude = gpsTracker.getLongitude();

        address = getCurrentAddress(latitude, longitude);
        String[] local = address.split(" ");
        String localName = local[2];

        readExcel(localName); //행정시 이름으로 격자값 구하기
        
        String weather = "";
          WeatherData wd = new WeatherData();
            try {
            // date와 time에 값을 넣어야함
            // ex) date = "20210722", time = "0500"
                weather = wd.lookUpWeather(date, time, x, y);
            } catch (IOException e) {
                Log.i("THREE_ERROR1", e.getMessage());
            } catch (JSONException e) {
                Log.i("THREE_ERROR2", e.getMessage());
            }
            Log.i("현재날씨",weather);
    }
    
      public void readExcel(String localName) {

        try {
            InputStream is = getBaseContext().getResources().getAssets().open("local_name.xls");
            Workbook wb = Workbook.getWorkbook(is);

            if (wb != null) {
                Sheet sheet = wb.getSheet(0);   // 시트 불러오기
                if (sheet != null) {
                    int colTotal = sheet.getColumns();    // 전체 컬럼
                    int rowIndexStart = 1;                  // row 인덱스 시작
                    int rowTotal = sheet.getColumn(colTotal - 1).length;

                    for (int row = rowIndexStart; row < rowTotal; row++) {
                        String contents = sheet.getCell(0, row).getContents();
                        if (contents.contains(localName)) {
                            x = sheet.getCell(1, row).getContents();
                            y = sheet.getCell(2, row).getContents();
                            row = rowTotal;
                        }
                    }
                }
            }
        } catch (IOException e) {
            Log.i("READ_EXCEL1", e.getMessage());
            e.printStackTrace();
        } catch (BiffException e) {
            Log.i("READ_EXCEL1", e.getMessage());
            e.printStackTrace();
        }
        Log.i("격자값", "x = " + x + "  y = " + y);
    }
 }