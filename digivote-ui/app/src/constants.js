
const cfg = {
  api: {
    cla: {
      baseUrl: "https://cla.cyber.stmarytx.edu",
      resources: {
        voters: "/voters",
        participants: "/voters?only_participants=true",
        validate: "/validate"
      }
    },
    ctf: {
      baseUrl: "https://ctf.cyber.stmarytx.edu",
      resources: {
        ballot: "/ballot",
        vote: "/vote",
      }
    }
  }
}

export default Object.freeze(cfg);