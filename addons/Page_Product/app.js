// ===============================
// Variables globales
// ===============================
let odooUrl = "";
let odooDb = "";
let odooUser = "";
let odooPassword = "";

let odooUid = null;
let odooSessionId = null;

// ===============================
// Helpers UI
// ===============================
function setLoading(isLoading) {
  const loadingZone = document.getElementById("loading-zone");
  if (!loadingZone) return;
  loadingZone.classList.toggle("hidden", !isLoading);
}

function showError(message) {
  const errorZone = document.getElementById("error-zone");
  if (!errorZone) return;

  if (message) {
    errorZone.textContent = message;
    errorZone.classList.remove("hidden");
  } else {
    errorZone.textContent = "";
    errorZone.classList.add("hidden");
  }
}

function clearProducts() {
  const grid = document.getElementById("products-grid");
  if (grid) {
    grid.innerHTML = "";
  }
}

// Affichage simple des produits (sera amélioré à l’exo 6.3)
function displayProducts(products) {
  const grid = document.getElementById("products-grid");
  if (!grid) return;

  clearProducts();

  if (!products || products.length === 0) {
    grid.innerHTML = "<p>Aucun produit trouvé.</p>";
    return;
  }

  products.forEach((p) => {
    const card = document.createElement("div");
    card.className = "product-card";

    const name = p.name || "(Sans nom)";
    const price =
      typeof p.list_price === "number" ? p.list_price.toFixed(2) : "0.00";
    const type = p.type || "inconnu";
    const ref = p.default_code || "-";
    const categName =
      Array.isArray(p.categ_id) && p.categ_id.length >= 2
        ? p.categ_id[1]
        : "Non catégorisé";
    const qty =
      typeof p.qty_available === "number" ? p.qty_available : 0;

    card.innerHTML = `
      <div class="product-name">${name}</div>
      <div class="product-meta">
        <div>Prix : ${price} €</div>
        <div>Type : ${type}</div>
        <div>Référence : ${ref}</div>
        <div>Catégorie : ${categName}</div>
        <div>Stock : ${qty}</div>
      </div>
    `;

    grid.appendChild(card);
  });
}

// ===============================
// authenticate() – Exercice 6.2
// ===============================
async function authenticate() {
  // 1. Récupérer les valeurs des inputs
  odooUrl = document.getElementById("odoo-url").value.trim();
  odooDb = document.getElementById("odoo-db").value.trim();
  odooUser = document.getElementById("odoo-user").value.trim();
  odooPassword = document.getElementById("odoo-password").value;

  if (!odooUrl || !odooDb || !odooUser || !odooPassword) {
    throw new Error("Merci de remplir tous les champs de configuration.");
  }

  // 2. URL de l’endpoint
  const endpoint =
    odooUrl.replace(/\/+$/, "") + "/web/session/authenticate";

  // 3. Payload JSON-RPC 2.0
  const payload = {
    jsonrpc: "2.0",
    method: "call",
    params: {
      db: odooDb,
      login: odooUser,
      password: odooPassword,
    },
    id: Math.floor(Math.random() * 1_000_000_000),
  };

  // 4. Appel fetch()
  let response;
  try {
    response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(payload),
    });
  } catch (err) {
    console.error("Erreur réseau (authenticate):", err);
    // TypeError = souvent CORS ou serveur down
    if (err instanceof TypeError) {
      throw new Error(
        "Failed to fetch : vérifie que Odoo tourne bien sur l’URL indiquée et qu’il n’y a pas de blocage CORS."
      );
    }
    throw err;
  }

  if (!response.ok) {
    throw new Error(
      `Erreur HTTP lors de l'authentification : ${response.status}`
    );
  }

  const data = await response.json();

  if (data.error) {
    console.error("Erreur Odoo authenticate:", data.error);
    throw new Error(
      "Échec de l'authentification : " +
        (data.error.data?.message || "voir console")
    );
  }

  if (!data.result || !data.result.uid) {
    throw new Error("Réponse d'authentification invalide.");
  }

  odooUid = data.result.uid;

  // Optionnel : récupérer le session_id dans les cookies
  try {
    const cookies = document.cookie.split(";").map((c) => c.trim());
    const sessionCookie = cookies.find((c) =>
      c.startsWith("session_id=")
    );
    if (sessionCookie) {
      odooSessionId = sessionCookie.split("=")[1];
    }
  } catch (e) {
    // pas bloquant
  }

  return odooUid;
}

// ===============================
// callOdoo() – Exercice 6.2
// ===============================
async function callOdoo(model, method, args = [], kwargs = {}) {
  if (!odooUrl) {
    throw new Error(
      "L'URL Odoo n'est pas définie. Appelle authenticate() d'abord."
    );
  }

  const endpoint =
    odooUrl.replace(/\/+$/, "") + "/web/dataset/call_kw";

  const payload = {
    jsonrpc: "2.0",
    method: "call",
    params: {
      model: model,
      method: method,
      args: args,
      kwargs: kwargs,
    },
    id: Date.now(),
  };

  let response;
  try {
    response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(payload),
    });
  } catch (err) {
    console.error("Erreur réseau (callOdoo):", err);
    if (err instanceof TypeError) {
      throw new Error(
        "Failed to fetch : vérifie que Odoo est accessible (URL/port) et les règles CORS."
      );
    }
    throw err;
  }

  if (!response.ok) {
    throw new Error(
      `Erreur HTTP lors de l'appel Odoo : ${response.status}`
    );
  }

  const data = await response.json();

  if (data.error) {
    console.error("Erreur Odoo call_kw:", data.error);
    throw new Error(
      data.error.data?.message ||
        "Erreur lors de l’appel Odoo (voir console)."
    );
  }

  return data.result;
}

// ===============================
// loadProducts() – Exercice 6.2
// ===============================
async function loadProducts() {
  showError("");
  setLoading(true);
  clearProducts();

  try {
    // 1. Authentification
    await authenticate();

    // 2. Champs à récupérer
    const fields = [
      "name",
      "list_price",
      "type",
      "default_code",
      "categ_id",
      "qty_available",
    ];

    // 3. Appel search_read sur product.template
    const domain = []; // pas de filtre pour le moment
    const products = await callOdoo(
      "product.template",
      "search_read",
      [domain],
      {
        fields: fields,
        limit: 50,
      }
    );

    // 4. Affichage
    displayProducts(products);
  } catch (err) {
    console.error("Erreur loadProducts:", err);
    showError(
      err.message ||
        "Erreur inconnue lors du chargement des produits."
    );
  } finally {
    setLoading(false);
  }
}

// ===============================
// Liaison du bouton après chargement du DOM
// ===============================
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("load-btn");
  if (btn) {
    btn.addEventListener("click", () => {
      loadProducts();
    });
  }
});
