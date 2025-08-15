# main.py
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from bson import ObjectId

# Cargar variables de entorno
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # 🔑 1. Configurar la clave secreta
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

    # --- NUEVO: CONFIGURACIÓN DE FLASK-LOGIN ---
    login_manager = LoginManager()
    login_manager.init_app(app)
    # Redirige a los usuarios no autenticados a la ruta de login
    login_manager.login_view = 'auth.login'

    # 👤 2. Definir el user_loader
    from app.models import User 
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)
    # --- FIN DE LA CONFIGURACIÓN DE FLASK-LOGIN ---

    # ➕ 3. Registrar TODOS tus blueprints
    from app.routes.main_routes import main_bp
    from app.auth_routes import auth_bp 
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

# Instancia la aplicación
app = create_app()

if __name__ == '__main__':
    # Ejecutar en modo desarrollo
    app.run(host='0.0.0.0', port=5000, debug=True)