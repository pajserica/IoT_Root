

const mongoose = require("mongoose");
let Schema = mongoose.Schema;

let postSchema = new Schema(
  {
    sensor: {
      type: String,
    },
    value: {
      type: String,
    },
    result: {
      type: String,
    },
  },
  { timestamps: true }
);

let Post = mongoose.model("senzor_kise", postSchema);

module.exports = Post;