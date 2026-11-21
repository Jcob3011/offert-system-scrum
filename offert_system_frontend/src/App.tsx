import {useState, useEffect} from "react";
import type {Offer} from "./types/offer.ts";
import {fetchOffers, loginUser} from "./api/offersApi.ts";

function App(){
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [offers, setOffers] = useState<Offer[]>([]);
  const [isLoggedIn, setIsLoggedIn] = useState(
      Boolean(localStorage.getItem('access_token'))
  );
  const [error, setError] = useState("");

  const handleLogin = async (e:React.FormEvent) => {
    e.preventDefault();
    setError('');
    try{
      await loginUser(username, password);
      setIsLoggedIn(true);
      const data = await fetchOffers();
      setOffers(data);
    }
    catch{
      setError('Błędny Login lub hasło!');
    }
  };

  const handleLoadOffers = async () => {
    try {
      const data = await fetchOffers();
      setOffers(data);
    } catch {
      setError('Nie udało się pobrać ofert (sprawdź czy token jest ważny).');
    }
  };
  useEffect(() => {
    if (!isLoggedIn) return;
    fetchOffers()
        .then((data) => setOffers(data))
        .catch(() => setError('Nie udało się pobrać ofert (sprawdź czy token jest ważny).'));
  }, [isLoggedIn]);



  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setIsLoggedIn(false);
    setOffers([]);
  };
  return (
      <div style={{ maxWidth: '900px', margin: '40px auto', fontFamily: 'sans-serif' }}>
        <h1>System Ofertowania B2B</h1>
        {error && <p style={{ color: 'red', fontWeight: 'bold' }}>{error}</p>}
        {!isLoggedIn ? (
            <form onSubmit={handleLogin} style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
              <input
                  type="text"
                  placeholder="Login (np. admin)"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
              />
              <input
                  type="password"
                  placeholder="Hasło"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
              />
              <button type="submit">Zaloguj (JWT)</button>
            </form>
        ) : (
            <div>
              <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
                <button onClick={handleLoadOffers}>Odśwież listę ofert z Django</button>
                <button onClick={handleLogout}>Wyloguj</button>
              </div>
              <table border={1} cellPadding={10} style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                <tr>
                  <th>Numer Oferty</th>
                  <th>Status</th>
                  <th>Netto (PLN)</th>
                  <th>VAT (PLN)</th>
                  <th>Brutto (PLN)</th>
                </tr>
                </thead>
                <tbody>
                {offers.map((offer) => (
                    <tr key={offer.id}>
                      <td><strong>{offer.offer_number}</strong></td>
                      <td>{offer.status}</td>
                      <td>{offer.total_price}</td>
                      <td>{offer.total_vat}</td>
                      <td><strong>{offer.total_gross}</strong></td>
                    </tr>
                ))}
                </tbody>
              </table>
            </div>
        )}
      </div>
  );
}
export default App;
