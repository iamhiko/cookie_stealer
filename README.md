# cookie_stealer
Chrome, kullanıcı çerezlerini AES-256 şifreleme algoritması ile otomatik olarak şifreler ve bu şifreleme mekanizmasını işletim sisteminin şifreleme özelliklerine (Windows'ta DPAPI - Data Protection API) entegre eder. https://github.com/Krptyk/chromeDekrpt aracını biraz geliştirdim ve githubdan direkt olarak dosyayı indirerek kullanıcının bilgisayarında açar ve şifreyi çözer. Şifreyi çözdükten sonra masterkey.txt dosyası oluşur ve cookielerle beraber gmail hesabına gönderir. chromeDekrpt kullanarak kendi bilgisayarınızda oturum açma bilgilerini elde edebilirsiniz. Pathları ve email girişlerini kodda değiştirmeyi unutmayın. Exeye çevirebilirsiniz. Daha etkili olması için ATtiny85 ile BAD USB yapıp dosyayı powershellden indirip açabilirsiniz. Sadece eğitim amaçlı kullanın illegal aktivitelerden ben sorumlu değilim.
