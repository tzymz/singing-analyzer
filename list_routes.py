from app.main import app

print("=== 所有注册的路由 ===")
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        methods = ', '.join(route.methods) if route.methods else 'ANY'
        print(f"{methods} {route.path}")
