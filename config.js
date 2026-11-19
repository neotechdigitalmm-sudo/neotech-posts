// Firebase-ის პარამეტრები (ვებ კონფიგურაცია საჯაროა, დაცვას firestore.rules აკეთებს).
export const firebaseConfig = {
  apiKey: 'AIzaSyAuzBtFtHdIeSatddgSpk7FF_Hf2RG4hgE',
  authDomain: 'neotech-marketing.firebaseapp.com',
  projectId: 'neotech-marketing',
  storageBucket: 'neotech-marketing.firebasestorage.app',
  messagingSenderId: '400507013267',
  appId: '1:400507013267:web:428f7461bdecae852c2566',
};

// ═══════ ბრენდის პარამეტრები: სხვა კომპანიისთვის მხოლოდ ეს ბლოკი, ფერები (index.html :root) და ლოგო იცვლება ═══════
export const BRAND = {
  name: 'ნეოტექი',                       // კომპანიის სახელი
  nameGen: 'ნეოტექის',                   // ნათესაობითი ბრუნვა („...ის პოსტი“)
  title: 'ნეოტექის მარკეტინგული სააგენტო', // საიტის სათაური
  logo: 'raw_logo.png',                  // ლოგოს ფაილი ამავე საქაღალდეში (თეთრი, გამჭვირვალე ფონით)
  shopUrl: 'https://shop.neotech.ge/',   // ონლაინ მაღაზია (ზედა მენიუ)
  shopHost: 'shop.neotech.ge',           // ბრენდ მენეჯერის ლინკი ამ დომენიდან უნდა იყოს
  loginDomain: 'neotech.local',          // შესვლის სახელი → სახელი@loginDomain (ნამდვილი ელფოსტა არ არის)
  // ბრენდ მენეჯერის მიმართულებები (რეგისტრაციისას აუცილებელი)
  cats: ['EZVIZ - ჭკვიანი სახლი', 'AJAX', 'ვიდეო მეთვალყურეობა', 'მონაცემთა შემნახველი', 'სახანძრო სისტემები', 'დაცვითი სიგნალიზაცია', 'დაშვების სისტემები', 'მონიტორები', 'ქსელური მოწყობილობები', 'კაბელები', 'ელექტრო საქონელი', 'ბრენდები'],
  // პოსტის სტილები, რომლებსაც ბრენდ მენეჯერი ირჩევს (link: 'shop' = მაღაზიის ლინკი, 'youtube' = YouTube ვიდეო)
  styles: {
    1: { name: 'სტილი 1', what: 'პოსტი + სთორი ვიდეო', need: 'პროდუქტის ლინკი shop.neotech.ge-ზე', link: 'shop' },
    2: { name: 'სტილი 2', what: 'მომწოდებლის YouTube ვიდეო ქართული ხმით', need: 'YouTube ვიდეოს ლინკი', link: 'youtube' },
    3: { name: 'სტილი 3', what: 'პროდუქტის ამხსნელი ვიდეო', need: 'პროდუქტის ლინკი shop.neotech.ge-ზე', link: 'shop' },
  },
  postDays: [2, 5],                      // საწყისი პოსტის დღეები (2 = სამშაბათი, 5 = პარასკევი); მერე მარკეტინგში იცვლება
  confirmHours: 3,                       // რამდენ საათში უნდა დაადასტუროს ბრენდ მენეჯერმა „100% გადამოწმებულია“
};
