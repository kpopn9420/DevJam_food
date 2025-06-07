import api from './api'

const Auth = {
  //Sign up for the system
  signUp: (body) => api.post('/auth/signup', body),
  // Sign in to the system
  signIn: (body) => api.post('/login', body),
  // Sign out of the system
  signOut: (body) => api.delete('/auth/signin', { data: body }),
  // Refresh the access token
  refresh: (body) => api.post('/auth/refresh', body),
  // Set password for the user
  setPassword: (body) => api.post('/auth/set-password', body),
  // Change the user's password
  changePassword: (body) => api.post('/auth/change-password', body),
  // Send a forget password email
  forgetPassword: (body) => api.post('/auth/forget-password', body),
}

export default Auth
