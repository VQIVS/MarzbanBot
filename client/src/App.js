import './App.css';
import ReactDom from 'react-dom';
function App() {
    return (
        <form className="wrapper">
            <h2>LOGIN</h2>
            <section className="group">
                <input
                    type="text"
                    size="30"
                    className="input"
                    name="email"
                    required
                />
                <label htmlFor="email" className="label">
                    Email
                </label>
            </section>
            <section className="group">
                <input
                    type="password"
                    minLength="8"
                    className="input"
                    name="password"
                    required
                />
                <label htmlFor="password" className="label">
                    Password
                </label>
            </section>
            <button type="button" className="btn">
                LOGIN
            </button>
            <span className="footer"></span>
        </form>
    );
}
export default App;