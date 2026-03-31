**HTTP POST: F12 > console > permitir colar**
fetch("https://script.google.com/macros/s/AKfycby29fdXEVRAxNugRG6HLLzHA1bNPTXPj8RNX3tR-srTXuBaftbcCJYXC9sn2j6VoYzK/exec", {
  method: "POST",
  mode: "no-cors", // Use isso se der erro de CORS, mas o Google costuma aceitar
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    temperatura: 28,
    umidade: 53
  })
})
.then(response => console.log("Enviado!"))
.catch(error => console.error("Erro:", error));

https://script.googleusercontent.com/macros/echo?user_content_key=AWDtjMXANwYu4z64jv1aORff4y2BAzz5qigfSlbehp4fESlKRykqPDyghGfqzJ56Wr-FkoljW1k1BzGJsbfOuz-msYACFAkszVGZPZZAYaC71eIxo3KcvTL6OIO3yv_38azvxKOYZM723NaoZUOVPrLMP7QRGb8-tkcUDJGnzx2Eowrnix9_x7Ifx1eKwOfNlaINIMAsZ-Zxx-kK2gcGPRqONGe6jQR4uBrnchPXHz9OnyFOUDWnR58K0OIAogwdMDGhc0isQ6OhrTWMAjSdb_-H7dCJbXsKLw&lib=MwFk5URydT4MHwuMz_cbDIkBOq5sxVIsY
