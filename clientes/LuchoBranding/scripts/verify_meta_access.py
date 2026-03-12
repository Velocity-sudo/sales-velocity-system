#!/usr/bin/env python3
"""Verifica acceso a todas las cuentas de Meta Ads configuradas."""
import json, urllib.request, urllib.error, ssl

CONFIG = "/Users/niko/Desktop/Clientes/LuchoBranding/config/clients_config.json"

def main():
    config = json.load(open(CONFIG))
    token = config["meta_app_token"]
    
    # 1. Validar token
    print("🔑 Validando token de Meta...")
    url = f"https://graph.facebook.com/v22.0/debug_token?input_token={token}&access_token={token}"
    try:
        ctx = ssl.create_default_context()
        data = json.loads(urllib.request.urlopen(url, timeout=10, context=ctx).read())
        d = data.get("data", {})
        if d.get("is_valid"):
            from datetime import datetime
            exp = datetime.fromtimestamp(d["expires_at"]).strftime("%Y-%m-%d")
            print(f"   ✅ Token VÁLIDO | Expira: {exp} | App: {d.get('application')}")
        else:
            print(f"   ❌ Token INVÁLIDO — necesitas renovar")
            return
    except Exception as e:
        print(f"   ⚠️ Error validando token: {e}")
        return

    # 2. Probar cada cuenta
    print("\n📊 Verificando acceso a cuentas de ads...\n")
    status_map = {1:"ACTIVE",2:"DISABLED",3:"UNSETTLED",7:"PENDING_REVIEW",
                  9:"IN_GRACE_PERIOD",100:"PENDING_CLOSURE",101:"CLOSED"}
    
    results = {"ok": [], "fail": [], "no_id": []}
    
    for key, client in config["clients"].items():
        name = client["name"]
        act_id = client.get("meta_ad_account_id", "")
        
        if not act_id:
            print(f"   ⬜ {name}: Sin Ad Account ID configurado")
            results["no_id"].append(name)
            continue
        
        url = f"https://graph.facebook.com/v22.0/{act_id}?fields=name,account_status,currency&access_token={token}"
        try:
            resp = json.loads(urllib.request.urlopen(url, timeout=10, context=ctx).read())
            s = status_map.get(resp.get("account_status", -1), "UNKNOWN")
            print(f"   ✅ {name}: {resp.get('name','?')} | Status: {s} | {resp.get('currency','?')}")
            results["ok"].append(name)
        except urllib.error.HTTPError as e:
            err = json.loads(e.read())
            code = err.get("error",{}).get("code","?")
            msg = err.get("error",{}).get("message","?")[:80]
            print(f"   ❌ {name} ({act_id}): Error {code} — {msg}")
            results["fail"].append(name)
        except Exception as e:
            print(f"   ⚠️ {name}: {e}")
            results["fail"].append(name)

    # Resumen
    print(f"\n{'='*50}")
    print(f"✅ Con acceso: {len(results['ok'])} — {', '.join(results['ok']) or 'ninguno'}")
    print(f"❌ Sin acceso: {len(results['fail'])} — {', '.join(results['fail']) or 'ninguno'}")
    print(f"⬜ Sin config: {len(results['no_id'])} — {', '.join(results['no_id']) or 'ninguno'}")

if __name__ == "__main__":
    main()
