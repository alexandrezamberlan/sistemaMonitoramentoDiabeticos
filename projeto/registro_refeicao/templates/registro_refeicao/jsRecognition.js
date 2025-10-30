    
    
    function startDictation() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert("Seu navegador não suporta a API de Reconhecimento de Voz.");
            return;
        
        let reconhecendo = false;
        let reconhecedor = new SpeechRecognition();

        {% comment %} if (reconhecendo) {
            reconhecedor.stop();
            return;
        } {% endcomment %}
      
    
        reconhecedor.lang = "pt-BR";  // Definir o idioma para português do Brasil
        reconhecedor.continuous = true;  // Continuar gravando até o usuário parar
        reconhecedor.interimResults = true;  // Resultados parciais enquanto a voz é reconhecida

        reconhecedor.onstart = function () {
            reconhecendo = true;
            document.getElementById("dictationBtn").innerHTML = "Parar de gravar";
        };

        reconhecedor.onend = function () {
            reconhecendo = false;
            document.getElementById("dictationBtn").innerHTML = "Iniciar gravação";
        };

        reconhecedor.onresult = function (event) {
            let transcript = "";
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            document.getElementById("id_registro_alimentacao").value = transcript;
            console.log("Transcrição atual: ", transcript);
        };

        reconhecedor.start();
    }