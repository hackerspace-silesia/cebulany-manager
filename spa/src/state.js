function now() {
  return Math.floor(new Date().getTime() / 1000);
}

export default {
  state: {
    deadline: now() + parseInt(localStorage.tokenTime || 0),
  },
  now: now,
  updateDeadline() {
    this.state.deadline = now() + parseInt(localStorage.tokenTime || 0);
  },
}
