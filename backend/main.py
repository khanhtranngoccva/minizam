from server.server import app

# Error handling
import server.error_handling

# All routes
import routes.identify

# Run Flask server
if __name__ == '__main__':
    app.run("0.0.0.0", 4000, debug=True)
