function now() {
  return Math.floor(new Date().getTime() / 1000);
}

export default {
  state: {
    deadline: now() + parseInt(sessionStorage.tokenTime || 0),
  },
  now: now,
  updateDeadline() {
    this.state.deadline = now() + parseInt(sessionStorage.tokenTime || 0);
  },
}
