import os
import requests

# El código buscará la clave de forma segura en las variables de entorno del sistema
API_KEY = os.environ.get("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai"

def consultar_tutor_ai(texto_usuario):
    # Verificación de seguridad local antes de realizar la petición web
    if not API_KEY:
        return (
            "Error: No se encontró la clave API en tu dispositivo.\n"
            "Asegúrate de configurar la variable de entorno 'OPENROUTER_API_KEY'."
        )

    headers = {
        "Authorization": f"Bearer {API_KEY.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost", 
        "X-Title": "Tutor Pydroid Continuo"
    }
    
    prompt_sistema = (
        "Eres un tutor de programación y ortografía amigable para un estudiante que aprende Python desde su celular. "
        "Analiza el texto o código del usuario. Si hay errores ortográficos o gramaticales, corrígelos. "
        "Si el usuario pide aprender algo de código, explícale de forma breve, "
        "muestra el código limpio y dale un pequeño tip útil para celular. Sé conciso y alentador."
    )
    
    data = {
        "model": "openrouter/free", 
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"Este es mi texto/código actual:\n\n{texto_usuario}"}
        ],
        "temperature": 0.7
    }
    
    print("\n[*] Enviando tu pregunta al Tutor IA...")
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        if response.status_code == 200:
            resultado = response.json()
            return resultado['choices'][0]['message']['content']
        else:
            return f"Error de la API ({response.status_code}): {response.text}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

if __name__ == "__main__":
    print("=== TUTOR CONTINUO EN PYDROID 3 ===")
    print("Escribe 'salir' en cualquier momento para terminar.\n")
    
    # Bucle continuo para mantener la conversación activa en la terminal
    while True:
        texto_usuario = input("\n¿Qué duda tienes o qué código quieres revisar?\n> ").strip()
        
        # Condición de salida para romper el ciclo de forma controlada
        if texto_usuario.lower() == 'salir':
            print("\n¡Adiós! Sigue practicando y escribiendo código. 🚀")
            break
            
        if texto_usuario != "":
            respuesta_ia = consultar_tutor_ai(texto_usuario)
            print("\n=== RESPUESTA Y LECCIÓN DEL TUTOR ===")
            print(respuesta_ia)
            print("=====================================")
        else:
            print("[*] Por favor escribe algo o escribe 'salir' para terminar.")
