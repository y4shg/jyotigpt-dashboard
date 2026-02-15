from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import requests
import os
from datetime import timedelta, datetime
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24).hex())
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Simple user store (in production, use a database)
USERS = {
    os.getenv('ADMIN_USERNAME', 'admin'): {
        'id': 1,
        'username': os.getenv('ADMIN_USERNAME', 'admin'),
        'password_hash': generate_password_hash(os.getenv('ADMIN_PASSWORD', 'changeme123'))
    }
}

@login_manager.user_loader
def load_user(user_id):
    for username, user_data in USERS.items():
        if user_data['id'] == int(user_id):
            return User(user_data['id'], user_data['username'])
    return None

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user_data = USERS.get(username)
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(user_data['id'], user_data['username'])
            login_user(user, remember=remember)
            session.permanent = True
            
            next_page = request.args.get('next')
            logger.info(f"User {username} logged in successfully")
            return redirect(next_page if next_page else url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            logger.warning(f"Failed login attempt for username: {username}")
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logger.info(f"User {current_user.username} logged out")
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

# API Routes
@app.route('/api/hf/spaces')
@login_required
def get_hf_spaces():
    """Fetch HuggingFace Spaces information"""
    try:
        hf_token = os.getenv('HF_TOKEN')
        space_ids = os.getenv('HF_SPACE_IDS', '').split(',')
        
        if not hf_token:
            return jsonify({'error': 'HuggingFace token not configured'}), 400
        
        if not space_ids or space_ids == ['']:
            return jsonify({'error': 'No space IDs configured'}), 400
        
        spaces_data = []
        headers = {'Authorization': f'Bearer {hf_token}'}
        
        for space_id in space_ids:
            space_id = space_id.strip()
            if not space_id:
                continue
                
            try:
                response = requests.get(
                    f"https://huggingface.co/api/spaces/{space_id}",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    space_data = response.json()
                    spaces_data.append({
                        'id': space_id,
                        'name': space_data.get('id', space_id),
                        'status': space_data.get('runtime', {}).get('stage', 'unknown'),
                        'hardware': space_data.get('runtime', {}).get('hardware', 'cpu-basic'),
                        'sdk': space_data.get('sdk', 'unknown')
                    })
                else:
                    logger.warning(f"Failed to fetch space {space_id}: {response.status_code}")
                    spaces_data.append({
                        'id': space_id,
                        'name': space_id,
                        'status': 'error',
                        'error': f'HTTP {response.status_code}'
                    })
            except Exception as e:
                logger.error(f"Error fetching space {space_id}: {str(e)}")
                spaces_data.append({
                    'id': space_id,
                    'name': space_id,
                    'status': 'error',
                    'error': str(e)
                })
        
        return jsonify(spaces_data)
            
    except Exception as e:
        logger.error(f"HF Spaces request failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/hf/space/<path:space_id>/restart', methods=['POST'])
@login_required
def restart_hf_space(space_id):
    """Restart a HuggingFace Space"""
    try:
        hf_token = os.getenv('HF_TOKEN')
        
        if not hf_token:
            return jsonify({'error': 'HuggingFace token not configured'}), 400
        
        response = requests.post(
            f"https://huggingface.co/api/spaces/{space_id}/restart",
            headers={'Authorization': f'Bearer {hf_token}'},
            timeout=10
        )
        
        if response.status_code in [200, 202]:
            logger.info(f"Space {space_id} restarted by {current_user.username}")
            return jsonify({'success': True, 'message': f'Space {space_id} restart initiated'})
        else:
            logger.error(f"Failed to restart space {space_id}: {response.status_code}")
            return jsonify({'error': 'Failed to restart space'}), response.status_code
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Space restart request failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/hf/space/<path:space_id>/pause', methods=['POST'])
@login_required
def pause_hf_space(space_id):
    """Pause a HuggingFace Space"""
    try:
        hf_token = os.getenv('HF_TOKEN')
        
        if not hf_token:
            return jsonify({'error': 'HuggingFace token not configured'}), 400
        
        response = requests.post(
            f"https://huggingface.co/api/spaces/{space_id}/pause",
            headers={'Authorization': f'Bearer {hf_token}'},
            timeout=10
        )
        
        if response.status_code in [200, 202]:
            logger.info(f"Space {space_id} paused by {current_user.username}")
            return jsonify({'success': True, 'message': f'Space {space_id} paused'})
        else:
            return jsonify({'error': 'Failed to pause space'}), response.status_code
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Space pause request failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error='Page not found', code=404), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return render_template('error.html', error='Internal server error', code=500), 500

@app.errorhandler(403)
def forbidden(error):
    return render_template('error.html', error='Access forbidden', code=403), 403

if __name__ == '__main__':
    # Development server only - use gunicorn/uwsgi for production
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
