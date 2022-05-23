import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { withRouter } from '@/router/withRouter'
import './index.css'
// Import centrally managed url paths
import URLS from '@/request/url'
import axios from 'axios'

class Signup extends Component {
	state = {
		// account
		accountNumber: '',
		// password
		passWord: '',
		// Confirm Password
		confirmPassWord: '',
		// account input bottom border color
		accountBorderButtomColor: '#fff',
		// account word below
		accountErrorOpacity: 0,
		// password input box border color
		passwordBorderButtomColor: '#fff',
		// pasword word below
		passwordErrorOpacity: 0,
		// confirm password input box border color
		confirmPasswordBorderButtomColor: '#fff',
		// confirm pasword word below
		confirmPasswordErrorOpacity: 0,
		// Mouse style when searching
		cursor: 'default'
	}

	// Account data binding
	changeAccountNumber = (e) => {
		this.setState({ accountNumber: e.target.value });
	}

	// password data binding
	changePassWord = (e) => {
		this.setState({ passWord: e.target.value });
	}

	// Confirm Password Data Binding
	changeConfirmPassWord = (e) => {
		this.setState({ confirmPassWord: e.target.value });
	}

	// Verify account password registration is correct
	handleSignup = async () => {
		const { accountNumber, passWord, confirmPassWord } = this.state;
		// Account not filled
		if (!accountNumber || accountNumber.length === 0) {
			this.accountHint.innerHTML = 'Please enter your username!';
			this.setState({ accountBorderButtomColor: 'red', accountErrorOpacity: 1 });
		}
		// Not enough account numbers
		else if (accountNumber.length < 5) {
			this.accountHint.innerHTML = 'Account number must be greater than 5!';
			this.setState({ accountBorderButtomColor: 'red', accountErrorOpacity: 1 });
		}
		// Account number is too long
		else if (accountNumber.length > 16) {
			this.accountHint.innerHTML = 'Account number must be less than 16!';
			this.setState({ accountBorderButtomColor: 'red', accountErrorOpacity: 1 });
		}
		// password is missing
		else if (!passWord || passWord.length === 0) {
			this.passwordHint.innerHTML = 'Please enter your password!';
			this.setState({ passwordBorderButtomColor: 'red', passwordErrorOpacity: 1 });
		}
		// Password is not enough
		else if (passWord.length < 8) {
			this.passwordHint.innerHTML = 'Password number must be greater than 8!';
			this.setState({ passwordBorderButtomColor: 'red', passwordErrorOpacity: 1 });
		}
		// Password is too long
		else if (passWord.length > 16) {
			this.passwordHint.innerHTML = 'Password number must be less than 16!';
			this.setState({ passwordBorderButtomColor: 'red', passwordErrorOpacity: 1 });
		}
		// Confirm password is not filled
		else if (!confirmPassWord || confirmPassWord.length === 0) {
			this.confirmPasswordHint.innerHTML = 'Please enter your confirm password!';
			this.setState({ confirmPasswordBorderButtomColor: 'red', confirmPasswordErrorOpacity: 1 });
		}
		// The two passwords do not match
		else if (passWord && confirmPassWord && passWord !== confirmPassWord) {
			this.passwordHint.innerHTML = 'The two passwords are inconsistent!';
			this.confirmPasswordHint.innerHTML = 'The two passwords are inconsistent!';
			this.setState({ passwordBorderButtomColor: 'red', passwordErrorOpacity: 1 });
			this.setState({ confirmPasswordBorderButtomColor: 'red', confirmPasswordErrorOpacity: 1 });
		}
		// If you have an account and a password, and the password is the same twice, you can send a request
		else if (accountNumber && passWord && confirmPassWord && accountNumber.length >= 5 && passWord.length >= 8 && passWord === confirmPassWord) {
			const requestParams = {
				account: accountNumber,
				password: passWord
			};
			this.setState({ cursor: 'wait' });
			// send request
			let res = await axios.post(URLS.USER_SIGN_UP, requestParams);
			let { body } = res.data;

			// 1 means registration is successful, 2 means registration fails
			switch (body) {
				case "1":
					alert('Signup success!');
					// Successful registration, jump to the login interface (deliberately stuck)
					setTimeout(() => {
						this.props.navigate("/login");
						this.setState({ cursor: 'default' });
					}, 500);
					break;
				case "2":
					// Registration fails (indicating that there are duplicate accounts), clear the three input boxes, and re-register
					alert('The account is duplicated, please re-enter the account!');
					this.setState({ accountNumber: '', passWord: '', confirmPassWord: '' });
					this.setState({ cursor: 'default' });
					break;
				case "3":
					// registration failed
					alert('Signup failed!');
					break;
				default:
					alert('Signup failed!');
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

	// confrim password input Box color recovery
	confirmPasswordRestoreInitial = () => {
		this.setState({ confirmPasswordBorderButtomColor: '#fff', confirmPasswordErrorOpacity: 0 })
	}

	render() {
		const { accountNumber, passWord, confirmPassWord } = this.state;
		return (
			<div className="signupUI">
				<div className="signup" style={{ cursor: this.state.cursor }}>
					<h2>User Signup</h2>
					<div className="signup_box">
						{/* required means that it cannot be empty. It must play a big role in the css effect. */}
						{/* Can be abbreviated as required */}
						<input
							type="text"
							required
							value={accountNumber}
							style={{ borderBottomColor: this.state.accountBorderButtomColor }}
							onFocus={this.accountRestoreInitial}
							onChange={e => this.changeAccountNumber(e)}
						/>
						<label>Your Username</label>
						<div ref={c => this.accountHint = c} style={{ marginTop: '-25px', color: 'red', opacity: this.state.accountErrorOpacity }}>Please input your username!</div>
					</div>
					<div className="signup_box">
						<input
							type="password"
							required
							value={passWord}
							style={{ borderBottomColor: this.state.passwordBorderButtomColor }}
							onChange={e => this.changePassWord(e)}
							onFocus={this.passwordRestoreInitial}
						/>
						<label>Your Password</label>
						<div ref={c => this.passwordHint = c} style={{ marginTop: '-25px', color: 'red', opacity: this.state.passwordErrorOpacity }}>Please input your password!</div>
					</div>
					<div className="signup_box">
						<input
							type="password"
							required
							value={confirmPassWord}
							style={{ borderBottomColor: this.state.confirmPasswordBorderButtomColor }}
							onChange={e => this.changeConfirmPassWord(e)}
							onFocus={this.confirmPasswordRestoreInitial}
						/>
						<label>Confirm Password</label>
						<div ref={c => this.confirmPasswordHint = c} style={{ marginTop: '-25px', color: 'red', opacity: this.state.confirmPasswordErrorOpacity }}>Please input your confirm password!</div>
					</div>
					<div className="login_bottom">
						<Link
							className="bottom_btn"
							to="/login"
						>
							Back to login
						</Link>
						<button
							className="bottom_btn"
							// to="/login"
							onClick={this.handleSignup}
						>
							Signup
						</button>
					</div>
				</div>
			</div>
		)
	}
}

export default withRouter(Signup)