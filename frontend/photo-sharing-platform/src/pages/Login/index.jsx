import React, { Component } from 'react'
import { Link } from "react-router-dom";
import { withRouter } from '@/router/withRouter'
import './index.css'
// Import centrally managed url paths
import URLS from '@/request/url'
import axios from 'axios'

class Login extends Component {
	componentDidMount() {
		const logedInAccount = JSON.parse(localStorage.getItem('Account'));
		if (logedInAccount) {
			this.setState({ accountNumber: logedInAccount.account, passWord: logedInAccount.password });
		}
	}

	state = {
		// account
		accountNumber: '',
		// password
		passWord: '',
		// account input bottom border color
		accountBorderButtomColor: '#fff',
		// account word below
		accountErrorOpacity: 0,
		// password input box border color
		passwordBorderButtomColor: '#fff',
		// pasword word below
		passwordErrorOpacity: 0,
		// Mouse style when searching
		cursor: 'default'
	}

	// data binding
	changeAccountNumber = (e) => {
		this.setState({ accountNumber: e.target.value });
	}

	// data binding
	changePassWord = (e) => {
		this.setState({ passWord: e.target.value });
	}

	// Login authentication
	handleLogin = async () => {
		const { accountNumber, passWord } = this.state;
		// account is missing
		if (!accountNumber || accountNumber.length === 0) {
			this.accountHint.innerHTML = 'Please enter your username!';
			this.setState({ accountBorderButtomColor: 'red', accountErrorOpacity: 1 });
		}
		// password is missing
		if (!passWord || passWord.length === 0) {
			this.passwordHint.innerHTML = 'Please enter your password!';
			this.setState({ passwordBorderButtomColor: 'red', passwordErrorOpacity: 1 });
		}
		if (accountNumber.length && passWord.length) {
			const requestParams = {
				account: accountNumber,
				password: passWord
			}
			this.setState({ cursor: 'wait' });

			let res = await axios.post(URLS.LOG_IN_VERIFICATION, requestParams);

			let { body } = res.data;
			console.log(body)
			this.setState({ cursor: 'default' });
			// 1 means account error, 2 means password error, 3 means success
			switch (body) {
				case "1":
					this.accountHint.innerHTML = 'Username not found. Please signup first!';
					this.setState({ accountBorderButtomColor: 'red', accountErrorOpacity: 1 });
					break;
				case "2":
					this.passwordHint.innerHTML = 'Password entered incorrectly!'
					this.setState({ passwordBorderButtomColor: 'red', passwordErrorOpacity: 1 });
					break;
				case "3":
					let accountLocalStorage = {
						account: accountNumber,
						password: passWord,
					};
					localStorage.setItem('Account', JSON.stringify(accountLocalStorage));
					this.props.navigate("/home");
					break;
				default:
					break;
			}
		}
	}

	// account input Box color recovery
	accountRestoreInitial = () => {
		this.setState({ accountBorderButtomColor: '#fff', accountErrorOpacity: 0 })
	}

	// password input Box color recovery
	passwordRestoreInitial = () => {
		this.setState({ passwordBorderButtomColor: '#fff', passwordErrorOpacity: 0 })
	}

	render() {
		const { accountNumber, passWord } = this.state;
		return (
			<div className="loginUI">
				<div className="login" style={{ cursor: this.state.cursor }}>
					<h2>User Login</h2>
					<div className="login_box">
						{/* required means that it cannot be empty. It must play a big role in the css effect. */}
						{/* Can be abbreviated as required */}
						<input
							type="text"
							className="login_input"
							required
							value={accountNumber}
							style={{ borderBottomColor: this.state.accountBorderButtomColor }}
							onChange={e => this.changeAccountNumber(e)}
							onFocus={this.accountRestoreInitial}
						/>
						<label>Username</label>
						<div ref={c => this.accountHint = c} style={{ marginTop: '-25px', color: 'red', opacity: this.state.accountErrorOpacity }}>Please input your username!</div>
					</div>
					<div className="login_box">
						<input
							type="password"
							className="login_input"
							required="required"
							value={passWord}
							style={{ borderBottomColor: this.state.passwordBorderButtomColor }}
							onChange={e => this.changePassWord(e)}
							onFocus={this.passwordRestoreInitial}
						/>
						<label>Password</label>
						<div ref={c => this.passwordHint = c} style={{ marginTop: '-25px', color: 'red', opacity: this.state.passwordErrorOpacity }}>Please input your password!</div>
					</div>

					<div className="login_bottom">
						{/* login button */}
						<button
							className="bottom_btn1"
							// to="/main"
							onClick={ this.handleLogin }
						>
							Login
						</button>
						{/* signup button */}
						<Link
							className="bottom_btn2"
							to="/signup"
						>
							Signup
						</Link>
					</div>
				</div>
			</div>
		)
	}
}

export default withRouter(Login)