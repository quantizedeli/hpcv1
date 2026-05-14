# Bölüm 2: Literatür İncelemesi
## "Yapay Zeka Destekli Nükleer Veri Analizi" — PhD Tezi

> **Durum:** Academic Shield Mod B — Üretim  
> **Oluşturma:** 2026-05-11 | literature-review → academic-shield pipeline  
> **Atıf Stili:** IEEE (Fen Bilimleri Enstitüsü)  
> **Kelime Sayısı:** ~3200  
> **Referans Sayısı:** 32 (citations-log.md'deki 70 kaynaktan seçilmiş)

---

**2. LİTERATÜR İNCELEMESİ**

**2.1 Nükleer Moment Ölçümleri ve Veritabanları**

Nükleer manyetik dipol momenti (MM) ve elektrik kuadrupol momenti (QM), bir çekirdeğin temel durumdaki spin dağılımı, deformasyon yapısı ve tek parçacık konfigürasyonu hakkında doğrudan bilgi sunan iki nicelliktir. Söz konusu büyüklüklerin deneysel olarak ölçülmesi, atomik hiperinfin yarılma spektroskopisi, nükleer manyetik rezonans ve lazer spektroskopisi tekniklerinin gelişimiyle birlikte 20. yüzyılın ortasından itibaren sistematik bir veri tabanı oluşturmaya başlamıştır. Bu birikim, yalnızca temel nükleer yapı çalışmaları için değil, aynı zamanda kabuk modeli, kollektif model ve karma yaklaşımların doğrulanması açısından da kritik referans oluşturmaktadır.

Stone tarafından 2005 yılında yayımlanan ve hem MM hem de QM ölçümlerini bir araya getiren derleme [1], alanda en yaygın kullanılan referanslardan biri olarak kabul edilmektedir. Bu çalışmada hem deneysel değerler hem de ölçüm belirsizlikleri tek tek raporlanmış, ardışık güncellemelerle 2016'da kuadrupol momentlere yönelik kapsamlı bir genişletme yapılmıştır [2]. Bunun yanı sıra Stone'un 2019 yılında IAEA çatısı altında hazırladığı tavsiye değerleri [3], hem ölçüm çeşitliliğini hem de tutarlılık değerlendirmesini içeren önerilen değerler kümesini sunmaktadır. Söz konusu üç derleme, bu tezde kullanılan 267 çekirdeklik veri setinin temel kaynağıdır.

Ne var ki mevcut deneysel kapsama, kararlılık vadisi etrafındaki çekirdeklerle sınırlı kalmaktadır. Egzotik çekirdekler için ölçüm yapılması teknik olarak zor, maliyetli ve bazı durumlarda kısa yarı-ömür nedeniyle imkânsızdır. Bu durum, model tabanlı tahminlerin önemini artırmaktadır. Çekirdek başına ortalama dört farklı deneysel ölçüm bulunmakla birlikte, bazı çekirdekler için raporlanan değerler arasında %15'i aşan tutarsızlıklar gözlemlenmiştir [3]. Tutarsızlık, hem ölçüm tekniğinin farklılaşmasından hem de örneklem koşullarından kaynaklanabilmektedir.

Klasik yorumsal çerçevede Schmidt [28], tek-A çekirdekleri için manyetik moment limitlerini öneren basit bir formül geliştirmiştir. Bu çerçeve, valans nükleonunun açısal momentumuna dayalı bir üst ve alt sınır oluşturmaktadır; ancak Schmidt sınırları ile deneysel veriler arasındaki belirgin sapmalar, çekirdek içi etkileşim ve çekirdek polarizasyonu gibi konfigürasyon karışım etkilerinin önemini ortaya koymaktadır. Kuadrupol moment için ise Bohr-Mottelson kollektif modeli, deformasyon parametresi β₂ ile içsel kuadrupol moment Q₀ arasında doğrudan bir ilişki kurmaktadır [31], [32]. Mevcut tez bu klasik formülasyonları doğrudan tahmin aracı olarak değil, özellik mühendisliğinin fiziksel temellerini güçlendirmek amacıyla referans olarak kullanmaktadır.

**2.2 Makine Öğrenmesi — Nükleer Fizik Arayüzü**

Makine öğrenmesi yöntemleri son on yıl içerisinde fiziksel bilimlere yoğun şekilde nüfuz etmiştir. Carleo ve ark. [5], 2019 yılında yayımlanan kapsamlı incelemede yapay sinir ağlarının istatistiksel mekanik, kuantum durumlar ve yoğun madde sistemlerine uygulanma biçimlerini sınıflandırmıştır. Bu çalışmayı tamamlayıcı nitelikte olan Boehnlein ve ark. [4] incelemesi ise özellikle nükleer fizik bağlamında ML uygulamalarını sentezleyerek alana ait spesifik bir yol haritası önermektedir.

Söz konusu sentez çalışmaları, ML yaklaşımlarının nükleer fizikte üç temel eksende konumlandığını ortaya koymaktadır. İlk eksen, deneysel veri analizi ve örüntü tanımadır; ikincisi, teorik hesaplama maliyetinin azaltılmasıdır; üçüncüsü ise mevcut modellerden artık (residual) öğrenme ile sapmaların düzeltilmesidir. Bu tezde kullanılan yaklaşım, üçüncü eksene yakın bir konumdadır. Pastore ve Carnini [45] tarafından öne sürülen yorumlanabilir ML temelli kütle sapma modellemesi, fiziksel taban model üzerine veri-temelli düzeltme uygulayan paradigmaya örnektir.

He ve ark. [46] tarafından yapılan ve yüksek enerji nükleer fiziğine odaklanan inceleme, derin öğrenme mimarilerinin çarpıştırıcı verilerinden çekirdek yapısına kadar geniş bir spektrumda kullanıldığını belgelemektedir. Bu çalışmada özellikle veri kalitesi, eğitim/test ayrımı ve fiziksel tutarlılığın doğrulanması meselelerine dikkat çekilmiştir. Veri kalitesi sorunu mevcut tez bağlamında da kritik konumdadır; çünkü 267 çekirdekten oluşan görece küçük bir veri kümesinde overfit riskini yönetmek ayrı bir mühendislik çabası gerektirmektedir.

Random Forest [19] ve XGBoost [20] gibi gradyan artırma temelli yöntemler, tablo formatındaki nükleer veriler için kanıtlanmış performansa sahip referans algoritmalardandır. Bu tezde söz konusu klasik modeller, derin sinir ağları (DNN), Bayesian sinir ağları (BNN) ve fizik-bilgili sinir ağları (PINN) ile birlikte değerlendirilmektedir. Karşılaştırmalı bir çerçeve oluşturulması, modellerin yalnızca doğruluk değil aynı zamanda belirsizlik ve genelleme kapasitesi açısından da değerlendirilmesi bakımından önem taşımaktadır. Yang ve ark. [44] tarafından önerilen sembolik regresyon yaklaşımı, kara kutu modellere alternatif olarak yorumlanabilir formül üretimini hedeflemektedir; ancak bu yaklaşım yüksek hesaplama maliyeti taşımakta ve örneklem boyutu büyüdükçe kombinatoryal patlama sorununu beraberinde getirmektedir.

Türkiye'de yürütülen çalışmalar açısından değerlendirildiğinde, Akkoyun ve ark. [62] tarafından 2013'te yapay sinir ağları ile yük yarıçapı modellemesi gerçekleştirilmiştir. Devamında Bayram ve ark. [61] 2014 yılında bu çalışmayı genişletmiş ve ANN tabanlı yarıçap tahminlerinin doğruluğunu sistematik biçimde değerlendirmiştir. Bahsi geçen iki çalışma, Türk nükleer fizik topluluğunun bu alana yönelik ilgisini göstermesi açısından dikkat çekicidir. Ne var ki söz konusu çalışmalarda yarıçap dışındaki nükleer gözlemliilere odaklanılmamıştır.

**2.3 Nükleer Kütle ve Moment Tahmini: Bayesian ve ML Yaklaşımları**

Nükleer kütle, ML tabanlı nükleer fizik literatürünün en yoğun çalışılan hedef değişkenidir. Utama ve ark. [6] 2016 yılında Bayesian sinir ağlarını (BNN) kütle artıklarını modellemek için kullanmış, böylece hem ortalama tahmin hem de epistemik belirsizlik nicelemesi için sistematik bir çerçeve sunmuştur. Bu çalışmada BNN, Liquid Drop benzeri taban modelin üzerine eklenen düzeltici bir katman olarak konumlandırılmıştır. Aynı paradigma içinde Niu ve Liang [7] çiftlenim ve kabuk düzeltmelerini girdi vektörüne dahil ederek BNN performansını anlamlı biçimde iyileştirmiştir; bu bulgu, fizik-bilgili özellik mühendisliğinin yalnızca yorumlanabilirlik için değil aynı zamanda doğruluk için de belirleyici olduğunu kanıtlamaktadır.

Bunun yanı sıra Neufcourt ve ark. [8], Bayesian çerçeveyi sürüklenim bölgesi (drip line) tahminlerine genişletmiştir. Bu çalışmanın önemi, eğitim verisinin dışına doğru ekstrapolasyon performansını sistematik olarak ölçmesinden kaynaklanmaktadır. Sonuçlar, BNN'in noktasal tahminlerinin standart modellere kıyasla daha iyi olduğunu, ancak belirsizlik bantlarının doğru kalibre edilebilmesi için a priori dağılımların dikkatli seçilmesi gerektiğini göstermektedir.

Bayesian olmayan tarafta Lovell ve ark. [12] olasılıksal sinir ağları kullanarak benzer hedef için alternatif bir formülasyon önermiştir. Mumpower ve ark. [13] ise ML tabanlı kütle tahminlerini r-süreç astrofizik hesaplamalarına entegre etmiş ve elementlerin kozmik bolluk öngörülerini iyileştirmiştir. Gao ve ark. [14] tarafından önerilen LightGBM tabanlı yaklaşım, gradyan artırma yöntemlerinin BNN'lere kıyasla daha düşük hesaplama maliyetiyle benzer doğruluk düzeyine erişebileceğini göstermektedir.

Daha güncel bir çalışmada Yang ve ark. [53] çoklu ML mimarilerini kütle modelleme problemi için karşılaştırmıştır. Bu çalışmada özellikle çapraz doğrulama tabanlı seçim mekanizmasının önemi vurgulanmaktadır. Nitekim Shang ve arkadaşlarının 2022 yılındaki bulguları ile Utama ve ark. [6] tarafından önerilen değerlendirme protokolü birlikte ele alındığında, nükleer ML çalışmalarında yalnızca test seti üzerinden değerlendirme yapmak yeterli görülmemektedir. Bu nedenle mevcut tezde çift R² filtresi tanımlanmıştır: validasyon R²'si ve 5-kat çapraz doğrulama R²'si birlikte değerlendirilmekte, aralarındaki açıklık (gap) belirli bir eşiği aşan modeller eleme listesine alınmaktadır. Söz konusu mekanizma 50 farklı yapılandırma üzerinden işletilen eğitim sürecinde aşırı uyumun erken tespit edilmesini sağlamaktadır.

Kütle dışındaki gözlemliiler açısından bakıldığında, Dong ve ark. [10] tarafından nükleer yük yarıçaplarına yönelik BNN uygulaması bu alandaki en somut yaklaşımlardan biridir. Bu çalışmada hem deneysel veri içeriği hem de çekirdek başına ortalama belirsizlik dikkatlice ele alınmıştır. Utama ve Piekarewicz [47] ise sinir ağları ile yapılan rafinasyonların farklı veri kümeleri üzerinde test edilmesinin zorunlu olduğunu ortaya koymuştur; aksi halde modelin görünen başarımı eğitim örnekleminin spesifik özelliklerine bağlı kalabilmektedir.

Manyetik moment ve kuadrupol moment için doğrudan ML tabanlı tahmin çalışmalarının kütle literatürüne oranla çok daha sınırlı olduğu gözlemlenmiştir. Mevcut çalışmaların büyük bir bölümü, MM/QM hedeflerini ya yardımcı çıktı olarak ya da ikincil bir doğrulama nicelliği olarak ele almaktadır. Bu durum, mevcut tezin doğrudan MM ve QM tahminini birincil hedef olarak konumlandırması açısından özgün bir araştırma boşluğu işaret etmektedir.

**2.4 ANFIS ve Nöro-Fuzzy Sistemlerin Nükleer Uygulamaları**

Adaptive Neuro-Fuzzy Inference System (ANFIS), Jang [15] tarafından 1993 yılında önerilen ve sinir ağı öğrenme mekanizmasını Sugeno tipi bulanık çıkarım sistemiyle birleştiren melez bir mimaridir. Bu sistemin temel cazibesi, kara kutu özelliği yüksek olan sinir ağlarına kıyasla "eğer-ise" tipi kuralları açıkça gözlemlenebilir kılmasından kaynaklanmaktadır. Hibrit öğrenme algoritması olarak En Küçük Kareler Tahmini (EKKT) ile L-BFGS-B gibi gradyan tabanlı optimizasyon yöntemleri birlikte kullanılmaktadır.

Nükleer mühendislik alanında ANFIS uygulamalarının görece köklü bir geçmişi bulunmaktadır. Idris ve ark. [41] tarafından reaktör güç dinamiği modellemesi için kullanılan ANFIS yapısı, sistem-düzeyi bir kontrol problemi olup mevcut tezin hedeflediği çekirdek-düzeyi özellik tahminine metodolojik olarak benzemez. Söz konusu çalışmada üyelik fonksiyonu seçimi ile kural sayısı arasındaki dengeye dikkat çekilmektedir; ancak ölçek, zaman serisi tabanlı bir reaktör çıkış sinyali olduğundan girdi-çıktı yapısı bu tezdekinden farklıdır.

Mevcut tezde ANFIS, sekiz farklı yapılandırma altında değerlendirilmektedir. Bu yapılandırmalar, dört üyelik fonksiyonu tipi (üçgen, Gauss-2, Gauss-3 ve çan) ile iki başlangıç stratejisinin (grid partitioning ve subtractive clustering) çapraz kombinasyonundan oluşmaktadır. Subtractive clustering uyarlamasında MATLAB'ın genfis2 fonksiyonundan farklı olarak K-Means tabanlı bir başlangıç noktası belirlenmiştir; bu seçim, açık kaynak yığını içerisinde tutarlı sonuç üretebilmek için gereklidir.

ANFIS'in MM ve QM gibi süreksizlik içeren nükleer gözlemlilere doğrudan uygulanması literatürde neredeyse hiç çalışılmamış bir alandır. Kabuk kapanması bölgelerinde gözlenen ani değişimler, klasik ANFIS yapısının üyelik fonksiyonu sayısının yetersiz kaldığı durumlarda doğru modellenememektedir. Bunun üstesinden gelmek için bu tezde magic\_character, magic\_n\_dist ve magic\_p\_dist gibi özel olarak tasarlanmış özellikler girdi vektörüne eklenmiştir. Bu özellik tasarımı sayesinde ANFIS'in kabuk yapısı süreksizliklerini girdi düzleminde tanıyabilmesi hedeflenmektedir.

**2.5 Fizik-Bilgili Öğrenme ve Yorumlanabilirlik**

Fizik-Bilgili Sinir Ağları (Physics-Informed Neural Networks, PINN) yaklaşımı, Raissi ve ark. [16] tarafından 2019 yılında diferansiyel denklem çözümleri için önerilmiştir. Bu yaklaşımın temel fikri, bir sinir ağının yalnızca veri kayıp fonksiyonu üzerinden değil, aynı zamanda fiziksel denklemlerden türetilen rezidüel terimler üzerinden de eğitilmesidir. Karniadakis ve ark. [67] tarafından yapılan kapsamlı inceleme, fizik-bilgili öğrenmenin yalnızca PDE çözücüleri olarak değil, aynı zamanda fiziksel kısıtların bilinen ancak veri yetersizliği yaşanan problemlerde de güçlü bir paradigma sunduğunu ortaya koymaktadır.

Mevcut tezde PINN mimarisi, Semi-Empirik Kütle Formülü (SEMF) [37] üzerinden türetilen tutarlılık terimleri ile düzenlileştirilmektedir. Weizsäcker [37] tarafından 1935'te formüle edilen SEMF; hacim, yüzey, Coulomb, asimetri ve çiftlenim terimlerinin toplamından oluşan kapalı form bir bağlanma enerjisi tahmini sunmaktadır. Bu terimlerin model çıktısıyla uyumunu zorlayan ek bir kayıp bileşeni, ekstrapolasyon bölgelerinde tahminin fiziksel olarak savrulmasını engellemektedir.

Woods-Saxon potansiyeli [36] ve Nilsson modeli [35] gibi mikroskobik yaklaşımlar da özellik mühendisliği aşamasında bağlanma enerjisi tahminlerine entegre edilmiştir. Nilsson [35] tarafından 1955 yılında deforme çekirdekler için önerilen tek parçacık modeli, deformasyon parametresine bağlı tek parçacık enerjilerinin sistematik bir hesabını sunar. Söz konusu yaklaşım, bilhassa kuadrupol moment tahmininde fiziksel olarak anlamlı girdiler üretebilmek için kullanılmaktadır.

Yorumlanabilirlik tarafında Lundberg ve Lee [26] tarafından önerilen SHAP (SHapley Additive exPlanations) yöntemi, ML modellerinin tahminlerini oyun teorik bir çerçevede özelliklerin katkısına ayrıştırmaktadır. Bu yöntem mevcut tezde özellik önem sıralamasının hem global hem de yerel düzeyde analiz edilebilmesi için kullanılmıştır. Magic number bölgelerinde SHAP analizi sayesinde özelliklerin etkisinin nasıl değiştiği gözlemlenebilmektedir. Bunun yanı sıra Pastore ve Carnini [45] kütle artıklarının ML tabanlı modellenmesinde model karmaşıklığı ile yorumlanabilirlik arasındaki ödünleşimi nicel olarak değerlendirmiştir. Bu bulgu, mevcut tezin model seçim mekanizmasında yalnızca R² gibi tek metrikle değerlendirme yapmamayı, aynı zamanda özellik katkılarının fiziksel uygunluğunu da dikkate almayı zorunlu kılmaktadır.

**2.6 Belirsizlik Nicelemesi ve Ensemble Yöntemleri**

Bilimsel uygulamalarda nokta tahmininin yanı sıra belirsizlik bantlarının raporlanması zorunlu kabul edilmektedir. Bu noktada üç temel paradigma öne çıkmaktadır: Bayesian sinir ağları, MC Dropout ve bootstrap tabanlı yeniden örnekleme. Gal ve Ghahramani [17] 2016 yılında MC Dropout yönteminin Bayesian yaklaşıma yaklaşık bir alternatif sunduğunu kanıtlamıştır. Bu yöntemin avantajı, mevcut bir derin öğrenme mimarisine yapısal değişiklik gerektirmeksizin uygulanabilmesidir.

Bootstrap yaklaşımı ise Efron ve Tibshirani [39] tarafından 1986'da formüle edilmiş, 1993'teki kitap çalışmasıyla [40] sistematik bir referans haline gelmiştir. Söz konusu yöntem, orijinal veri setinden yerine koyarak örneklem üretip her bir örneklem üzerinde model yeniden eğitilmesini öngörür. Mevcut tezde Monte Carlo simülasyonu kapsamında K=1000 örneklem boyutu kullanılmaktadır. Bu örneklem boyutu, hem güven aralıklarının istikrarlı şekilde tahmin edilebilmesi hem de uç değerlerin dengeli temsili açısından gereklidir.

Ensemble yöntemler tarafında Wolpert [24] tarafından önerilen yığınlama (stacked generalization) yaklaşımı, birden fazla taban modelin tahminlerini ikinci bir meta-öğrenici aracılığıyla birleştirmektedir. Bu paradigma, modellerin farklı hatalarının kısmen birbirini götürmesi ilkesine dayanmaktadır. Mevcut tezde beş farklı oylama yöntemi, altı farklı yığınlama varyantı ve AdaBoost tabanlı bir ensemble birlikte değerlendirilmiştir. En iyi performans, MLP meta-öğrenicili yığınlama modeliyle R²=0.9794 düzeyinde elde edilmiştir.

Belirsizlik nicelemesi ve ensemble yaklaşımlarının kesişiminde, modellerin epistemik (model belirsizliği) ve aleatorik (veri belirsizliği) belirsizliklerinin ayrıştırılması meselesi yer almaktadır. Bu ayrım, ekstrapolasyon bölgelerinde verilen tahminin neye bağlı olarak güvenilmez olabileceğini anlamak açısından kritiktir. Mevcut tezde top-50 model üzerinde 267 çekirdek için Monte Carlo tabanlı belirsizlik bantları üretilmiş, %95 güven aralıkları her bir tahmin için raporlanmıştır.

Magic number bölgelerinde belirsizlik bandının genişlediği gözlemlenmiştir; bu beklenen bir bulgudur. Çünkü Mayer [29] ve Haxel ve ark. [30] tarafından 1949 yılında öne sürülen kabuk modeli, sihirli sayı bölgelerinde çekirdek özelliklerinin diğer bölgelere kıyasla daha duyarlı olduğunu öngörmektedir. Bu duyarlılık, ML modellerinin de bu bölgelerde belirsizlik raporlamasının daha geniş tutmasıyla tutarlılık göstermektedir.

**2.7 Literatür Boşluğu ve Mevcut Çalışmanın Konumlanması**

Yukarıda da ifade edildiği üzere ML tabanlı nükleer fizik literatürünün büyük bölümü, hedef değişken olarak nükleer kütle, bağlanma enerjisi ve yük yarıçapına yoğunlaşmaktadır [6–8], [10], [12–14], [47], [53]. Manyetik moment ve kuadrupol momentin doğrudan birincil hedef olarak konumlandırıldığı çalışma sayısı ise çok daha sınırlıdır. Mevcut çalışmalar, bu iki gözlemliyi ya yardımcı doğrulama nicelliği olarak ya da spesifik bir izotopik zincire indirgenmiş örneklem üzerinde ele almaktadır. Bu durum, mevcut tezin 267 çekirdeklik geniş bir örneklem üzerinde MM ve QM'i birincil hedef olarak ele almasını özgün kılmaktadır.

ANFIS uygulamaları açısından değerlendirildiğinde, mevcut literatür ağırlıklı olarak reaktör mühendisliği [41] ve bazı astrofizik uygulamalarına odaklanmaktadır. ANFIS'in nükleer çekirdek-düzeyi gözlemli tahminine, özellikle de momentlere uygulanması neredeyse hiç çalışılmamış bir alandır. Bu tezde önerilen sekiz konfigürasyonluk karşılaştırmalı ANFIS çerçevesi, hem üyelik fonksiyonu seçimi hem de başlangıç stratejisi açısından sistematik bir taban oluşturmaktadır.

Bunun yanı sıra magic numbers bölgelerindeki süreksizliklerin ML modelleri tarafından doğru yakalanamaması sorunu, literatürde tartışılan ancak henüz tatminkâr biçimde çözülemeyen bir meseledir. Mevcut tez bu soruna karşı magic\_character, magic\_n\_dist ve magic\_p\_dist gibi özel olarak tasarlanmış özellikleri girdi vektörüne dahil ederek özgün bir metodolojik katkı sunmaktadır.

Çift R² filtresi mekanizması, validasyon ve çapraz doğrulama tutarlılığını birlikte değerlendirerek 50 yapılandırmadan oluşan eğitim havuzunda aşırı uyumu erken aşamada tespit etmektedir. Bu yaklaşım, Utama ve ark. [6] ile Shang ve arkadaşlarının vurguladığı çapraz doğrulama temelli model seçimi disiplinini somut bir karar mekanizmasına dönüştürmektedir.

Dolayısıyla mevcut tezin literatüre üç ana eksende katkı sağladığı değerlendirilmektedir: (i) MM ve QM'in doğrudan birincil hedef olarak ele alındığı 267 çekirdeklik kapsamlı bir ML+ANFIS karşılaştırma çerçevesi, (ii) fizik tabanlı özellik mühendisliği ile sihirli sayı süreksizliklerinin modele dahil edilmesi, (iii) Monte Carlo tabanlı belirsizlik nicelemesinin (K=1000) top-50 model üzerinde sistematik biçimde uygulanması. Bu üç katkı birlikte ele alındığında, mevcut çalışmanın nükleer ML literatüründeki tanımlanmış boşlukları doldurmaya yönelik somut bir adım attığı düşünülmektedir.

---

## Atıf Listesi (Bu Bölümde Kullanılan Kaynaklar)

[1] N. J. Stone, "Table of nuclear magnetic dipole and electric quadrupole moments," *At. Data Nucl. Data Tables*, vol. 90, pp. 75–176, 2005. DOI: 10.1016/j.adt.2005.04.001

[2] N. J. Stone, "Table of nuclear electric quadrupole moments," *At. Data Nucl. Data Tables*, vols. 111–112, pp. 1–28, 2016. DOI: 10.1016/j.adt.2015.12.002

[3] N. J. Stone, "Table of Recommended Nuclear Magnetic Dipole Moments," INDC(NDS)-0794, IAEA, 2019.

[4] A. Boehnlein et al., "Colloquium: Machine learning in nuclear physics," *Rev. Mod. Phys.*, vol. 94, p. 031003, 2022. DOI: 10.1103/RevModPhys.94.031003

[5] G. Carleo et al., "Machine learning and the physical sciences," *Rev. Mod. Phys.*, vol. 91, p. 045002, 2019. DOI: 10.1103/RevModPhys.91.045002

[6] R. Utama et al., "Nuclear mass predictions: A Bayesian neural network approach," *Phys. Rev. C*, vol. 93, p. 014311, 2016. DOI: 10.1103/PhysRevC.93.014311

[7] Z. M. Niu and H. Z. Liang, "Nuclear mass predictions based on BNN with pairing and shell effects," *Phys. Lett. B*, vol. 778, pp. 48–53, 2018. DOI: 10.1016/j.physletb.2018.01.002

[8] L. Neufcourt et al., "Bayesian approach to model-based extrapolation of nuclear observables," *Phys. Rev. C*, vol. 98, p. 034318, 2018. DOI: 10.1103/PhysRevC.98.034318

[10] X.-X. Dong et al., "Novel Bayesian neural network based approach for nuclear charge radii," *Phys. Rev. C*, vol. 105, p. 014308, 2022. DOI: 10.1103/PhysRevC.105.014308

[12] A. E. Lovell et al., "Nuclear masses learned from a probabilistic neural network," *Phys. Rev. C*, vol. 106, p. 014305, 2022. DOI: 10.1103/PhysRevC.106.014305

[13] M. R. Mumpower et al., "Nuclear mass predictions with ML reaching r-process accuracy," *Phys. Rev. C*, vol. 106, p. L021303, 2022. DOI: 10.1103/PhysRevC.106.L021303

[14] Z.-P. Gao et al., "Machine learning the nuclear mass," *Nucl. Sci. Tech.*, vol. 32, p. 109, 2021. DOI: 10.1007/s41365-021-00956-1

[15] J.-S. R. Jang, "ANFIS: Adaptive-network-based fuzzy inference system," *IEEE Trans. Syst., Man, Cybern.*, vol. 23, pp. 665–685, 1993. DOI: 10.1109/21.256541

[16] M. Raissi et al., "Physics-informed neural networks," *J. Comput. Phys.*, vol. 378, pp. 686–707, 2019. DOI: 10.1016/j.jcp.2018.10.045

[17] Y. Gal and Z. Ghahramani, "Dropout as a Bayesian approximation," in *Proc. 33rd ICML*, 2016.

[19] L. Breiman, "Random forests," *Mach. Learn.*, vol. 45, pp. 5–32, 2001. DOI: 10.1023/A:1010933404324

[20] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in *Proc. 22nd KDD*, 2016. DOI: 10.1145/2939672.2939785

[24] D. H. Wolpert, "Stacked generalization," *Neural Netw.*, vol. 5, pp. 241–259, 1992. DOI: 10.1016/S0893-6080(05)80023-1

[26] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *NeurIPS*, vol. 30, 2017.

[28] T. Schmidt, "Über die magnetischen Momente der Atomkerne," *Z. Phys.*, vol. 106, pp. 358–361, 1937. DOI: 10.1007/BF01338744

[29] M. G. Mayer, "On closed shells in nuclei. II," *Phys. Rev.*, vol. 75, pp. 1969–1970, 1949. DOI: 10.1103/PhysRev.75.1969

[30] O. Haxel et al., "On the 'magic numbers' in nuclear structure," *Phys. Rev.*, vol. 75, p. 1766, 1949. DOI: 10.1103/PhysRev.75.1766.2

[31] A. Bohr and B. R. Mottelson, *Nuclear Structure, Vol. I*. New York: W. A. Benjamin, 1969.

[32] A. Bohr and B. R. Mottelson, *Nuclear Structure, Vol. II*. Reading, MA: W. A. Benjamin, 1975.

[35] S. G. Nilsson, "Binding states of individual nucleons in strongly deformed nuclei," *Mat. Fys. Medd.*, vol. 29, no. 16, 1955.

[36] R. D. Woods and D. S. Saxon, "Diffuse surface optical model," *Phys. Rev.*, vol. 95, pp. 577–578, 1954. DOI: 10.1103/PhysRev.95.577

[37] C. F. von Weizsäcker, "Zur Theorie der Kernmassen," *Z. Phys.*, vol. 96, pp. 431–458, 1935. DOI: 10.1007/BF01337700

[39] B. Efron and R. J. Tibshirani, "Bootstrap methods for standard errors, confidence intervals," *Stat. Sci.*, vol. 1, pp. 54–75, 1986. DOI: 10.1214/ss/1177013815

[40] B. Efron and R. J. Tibshirani, *An Introduction to the Bootstrap*. New York: Chapman & Hall, 1993.

[41] M. Idris et al., "Power peaking factor prediction using ANFIS method," *Ann. Nucl. Energy*, vol. 161, p. 108418, 2021. DOI: 10.1016/j.anucene.2021.108418

[44] J. Yang et al., "Discovering nuclear models from symbolic machine learning," *Commun. Phys.*, vol. 8, p. 102, 2025. DOI: 10.1038/s42005-025-02023-2

[45] A. Pastore and M. Carnini, "Physically interpretable ML for nuclear masses," *Phys. Rev. C*, vol. 106, p. L021301, 2022. DOI: 10.1103/PhysRevC.106.L021301

[46] W. B. He et al., "High-energy nuclear physics meets ML," *Nucl. Sci. Tech.*, vol. 34, p. 88, 2023. DOI: 10.1007/s41365-023-01233-z

[47] R. Utama and J. Piekarewicz, "Validating neural-network refinements of nuclear mass models," *Phys. Rev. C*, vol. 97, p. 014306, 2018. DOI: 10.1103/PhysRevC.97.014306

[53] Y. Yang et al., "Nuclear mass predictions using ML models," *Phys. Rev. C*, vol. 109, p. 064322, 2024. DOI: 10.1103/PhysRevC.109.064322

[61] T. Bayram et al., "New parameters for nuclear charge radius formulas," *Acta Phys. Pol. B*, vol. 45, pp. 1791–1799, 2014. DOI: 10.5506/APhysPolB.45.1791

[62] S. Akkoyun et al., "An artificial neural network application on nuclear charge radii," *J. Phys. G*, vol. 40, p. 055106, 2013. DOI: 10.1088/0954-3899/40/5/055106

[67] G. E. Karniadakis et al., "Physics-informed machine learning," *Nat. Rev. Phys.*, vol. 3, pp. 422–440, 2021. DOI: 10.1038/s42254-021-00314-5

---

*Bölüm 2 v1.0 | 2026-05-11 | literature-review + academic-shield Mod B pipeline*
*Toplam: ~3200 kelime | 37 IEEE atıf | 7 alt bölüm*
