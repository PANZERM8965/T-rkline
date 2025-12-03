// Dark Mode Toggle
const themeBtn = document.getElementById("theme-toggle");
themeBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    themeBtn.textContent = document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
});

// Dil Toggle (TR/EN)
const langBtn = document.getElementById("lang-toggle");
let lang = "tr";

const translations = {
    tr: {
        heroTitle: "Türkline",
        heroText: "Yerel, Hızlı ve Güvenli Mesajlaşma Deneyimi",
        heroBtn: "Keşfet",
        featuresTitle: "Özellikler",
        features: [
            "Tüm konuşmalarınız gizli ve korumalı.",
            "Yerli bir uygulama, tamamen Türkçe arayüz.",
            "Düşük donanımlı cihazlarda bile sorunsuz çalışır."
        ],
        aboutTitle: "Türkline Hakkında",
        aboutText: "Türkline, Türkiye için geliştirilmiş yerli bir mesajlaşma uygulamasıdır. WhatsApp’a alternatif olarak, daha güvenli ve özgür bir iletişim deneyimi sunar.",
        downloadTitle: "Türkline'ı İndir",
        downloadButtons: ["📱 Android için İndir", "💻 Windows 10 & 11 için İndir"],
        reviewsTitle: "Kullanıcı Yorumları",
        reviews: [
            "⭐️⭐️⭐️⭐️⭐️ \"Gerçekten harika bir uygulama, WhatsApp yerine artık Türkline kullanıyorum!\" - Ayşe",
            "⭐️⭐️⭐️⭐️ \"Çok hızlı ve pratik, yerli olması da ayrı güven veriyor.\" - Mehmet"
        ],
        newsTitle: "Haberler & Duyurular",
        news: [
            "📢 Türkline v1.0 yayınlandı! (2025)",
            "🔜 Yakında grup sohbetleri özelliği geliyor."
        ],
        contactTitle: "İletişim"
    },
    en: {
        heroTitle: "Türkline",
        heroText: "Local, Fast and Secure Messaging Experience",
        heroBtn: "Explore",
        featuresTitle: "Features",
        features: [
            "All your chats are private and secure.",
            "A local app with a fully English interface.",
            "Runs smoothly even on low-end devices."
        ],
        aboutTitle: "About Türkline",
        aboutText: "Türkline is a local messaging app developed for Turkey. As an alternative to WhatsApp, it offers a safer and freer communication experience.",
        downloadTitle: "Download Türkline",
        downloadButtons: ["📱 Download for Android", "💻 Download for Windows 10 & 11"],
        reviewsTitle: "User Reviews",
        reviews: [
            "⭐️⭐️⭐️⭐️⭐️ \"Really amazing app, I now use Türkline instead of WhatsApp!\" - Ayşe",
            "⭐️⭐️⭐️⭐️ \"Very fast and practical, being local gives extra trust.\" - Mehmet"
        ],
        newsTitle: "News & Updates",
        news: [
            "📢 Türkline v1.0 released! (2025)",
            "🔜 Group chat feature coming soon."
        ],
        contactTitle: "Contact"
    }
};

langBtn.addEventListener("click", () => {
    lang = lang === "tr" ? "en" : "tr";
    document.body.style.opacity = 0;

    setTimeout(() => {
        // Hero
        document.querySelector(".hero h1").textContent = translations[lang].heroTitle;
        document.querySelector(".hero p").textContent = translations[lang].heroText;
        document.querySelector(".hero .btn").textContent = translations[lang].heroBtn;

        // Section Titles
        document.querySelector("#features h2").textContent = translations[lang].featuresTitle;
        document.querySelector("#about h2").textContent = translations[lang].aboutTitle;
        document.querySelector("#download h2").textContent = translations[lang].downloadTitle;
        document.querySelector("#reviews h2").textContent = translations[lang].reviewsTitle;
        document.querySelector("#news h2").textContent = translations[lang].newsTitle;
        document.querySelector("#contact h2").textContent = translations[lang].contactTitle;

        // Features
        document.querySelectorAll(".feature p").forEach((p,i)=>p.textContent = translations[lang].features[i]);

        // About
        document.querySelector(".about p").textContent = translations[lang].aboutText;

        // Download buttons
        const downloadBtns = document.querySelectorAll(".download-btn");
        downloadBtns.forEach((btn,i)=>btn.textContent = translations[lang].downloadButtons[i]);

        // Reviews
        document.querySelectorAll(".reviews .review p").forEach((p,i)=>p.textContent = translations[lang].reviews[i]);

        // News
        document.querySelectorAll(".news li").forEach((li,i)=>li.textContent = translations[lang].news[i]);

        document.body.style.opacity = 1;
    }, 200);
});
// Menü linkleri için akıcı scroll
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault(); // default hızlı jump engelle
        const targetId = this.getAttribute('href').slice(1);
        const target = document.getElementById(targetId);
        if(target) {
            window.scrollTo({
                top: target.offsetTop - 70, // navbar yüksekliği kadar boşluk
                behavior: 'smooth'
            });
        }
    });
});
