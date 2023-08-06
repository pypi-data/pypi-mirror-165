/*
 * Copyright (C) 2016-2022 T-Head Semiconductor Co., Ltd. All rights reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the License); you may
 * not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an AS IS BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/* CSI-NN2 version 2.0.x */

#ifndef INCLUDE_SHL_ASP_H_
#define INCLUDE_SHL_ASP_H_

#include "csi_nn.h"
#include "shl_ref.h"

int shl_asp_avgpool2d(struct csinn_tensor *input, struct csinn_tensor *output,
                      struct csinn_pool_params *params);
int shl_asp_conv2d(struct csinn_tensor *input, struct csinn_tensor *output,
                   struct csinn_tensor *kernel, struct csinn_tensor *bias,
                   struct csinn_conv2d_params *params);
int shl_asp_depthwise_conv2d(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);
int shl_asp_fullyconnected(struct csinn_tensor *input, struct csinn_tensor *output,
                           struct csinn_tensor *kernel, struct csinn_tensor *bias,
                           struct csinn_fc_params *params);
int shl_asp_maxpool2d(struct csinn_tensor *input, struct csinn_tensor *output,
                      struct csinn_pool_params *params);
#endif  // INCLUDE_SHL_ASP_H_
