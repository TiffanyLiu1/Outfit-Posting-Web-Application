import React, { Component } from 'react'
import { withRouter } from '@/router/withRouter'
import { Container, Row, Col } from 'react-bootstrap'
import URLS from '@/request/url'
import axios from 'axios'
import store from '@/redux/store'
import './index.css'

class ImgPage extends Component {
	// process like icon item click function
	processLikeClick = async (e) => {
		// jusge whether account expires
		const logedInAccount = JSON.parse(localStorage.getItem('Account')).account;

		// change icon from unlike to like
		const curImgId = e.currentTarget.getAttribute('data-id');
		const category = e.currentTarget.firstElementChild.getAttribute('data-category');

		if (category === 'heart') {
			// send axios to change the database
			const requestParams = {
				imgId: curImgId,
				account: logedInAccount
			}
			await axios.put(URLS.LIKED_STATUS_CHANGE, requestParams);
		} else if (category === 'cross') {
			if(window.confirm('Are you sure to delete this post?')) {
				// send axios to change the database
				const requestParams = {
					imgId: curImgId,
					account: logedInAccount
				}
				await axios.post(URLS.DELETE_IMAGE, requestParams);
				alert('Delete success!');
			}
		}

		this.props.setResultImage(curImgId, category);
	}

	processDetail = async (e) => {
		const curImgId = e.currentTarget.getAttribute('data-id');
		const requestParams = {
			imgId: curImgId,
			account: JSON.parse(localStorage.getItem('Account')).account
		};
		let res = await axios.post(URLS.IMAGE_DETAIL, requestParams);
		const { body } = res.data;
		store.dispatch({ type: 'imgDetail', data: body });
		this.props.navigate('/imgDetail');
	}

	render() {
		const { data } = this.props;
		let itemList = [];
		for (let item of data) {
			itemList.push(
				<Col
					className="colBox"
					key={item.imgId}
					sm={4} md={2}
				>
					<div
						className='imgBox'
						data-id={item.imgId}
						onClick={this.processDetail}
					>
						<img 
							src={item.src} 
							alt="img"
						/>
					</div>
					<div
						className='imgInfoBox'
						data-id={item.imgId}
						onClick={this.processLikeClick}
					>
						{
							item.liked !== undefined ?
								item.liked === true ? <i data-category="heart" className="fas fa-heart"></i> : <i data-category="heart" className="far fa-heart"></i>
								:
								<i data-category="cross" className="far fa-times-circle"></i>
						}
					</div>
				</Col>
			)
		}
		console.log('所有的:', itemList);

		return (
			<div>
				<Container className="mainContainer">
					{/* Stack the columns on mobile by making one full-width and the other half-width */}
					<Row>
						{itemList}
					</Row>
				</Container>
			</div>
		)
	}
}

export default withRouter(ImgPage)