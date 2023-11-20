<template>
	<div class="container">
		<h1 class="text-center mt-5">Sign Up</h1>
	
	
		<form @submit.prevent="handleSubmit" class="mx-auto mt-5 p-5 border rounded-3">
			<div class="mb-3 text-success">{{ success }}</div>

			<div class="mb-3">
				<label for="username" class="form-label">Username:</label>
				<input type="text" id="username" name="username" class="form-control" required>
			</div>

			<div class="mb-3">
				<label for="email" class="form-label">Email:</label>
				<input type="email" id="email" name="email" class="form-control" required>
			</div>

			<div class="mb-3">
				<label for="password" class="form-label">Password:</label>
				<input type="password" id="password" name="password" class="form-control" required>
			</div>

			<div class="mb-3">
				<label for="confirm_password" class="form-label">Confirm Password:</label>
				<input type="password" id="confirm_password" name="confirm_password" class="form-control" required>
			</div>

			<div class="mb-3 text-danger">{{ ans }}</div>

			<div class="d-grid">
				<input type="submit" value="Sign Up" class="btn btn-primary">
			</div>
		</form>
	</div>
</template>

<script>
import axios from '../axios';
export default {
	name: 'UserSignup',
	data() {
		return {
			ans: '',
			success: ""
		}
	},
	methods: {
		
		async handleSubmit() {
			const data = {
				username: document.getElementById('username').value,
				email: document.getElementById('email').value,
				password: document.getElementById('password').value,
				confirm_password: document.getElementById('confirm_password').value,
			}
			const response = await axios.post('signup', data)
			this.ans = response.data.message
			this.success = response.data.success
			if (response.data.success) {
				setTimeout(() => {
					this.$router.push('/login')
				}, 2000)
				
			}
			setTimeout(() => {
				this.ans = ''
				this.success = ''
			}, 2000)
		},
	}
}
</script>

<style scoped></style>