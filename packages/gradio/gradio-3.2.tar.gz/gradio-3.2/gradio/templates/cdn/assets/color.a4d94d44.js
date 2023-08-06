import { ae as ordered_colors } from './index.8da6a09f.js';

const get_next_color = (index) => {
  return ordered_colors[index % ordered_colors.length];
};

export { get_next_color as g };
