<template>
  <div class="p-8">
    <div class="mb-8">
      <h3 class="text-lg font-bold text-gray-900 mb-4">选择简历模板</h3>
      <div class="grid grid-cols-4 gap-4">
        <div
          @click="selectTemplate('classic')"
          :class="['border-2 rounded-xl p-4 cursor-pointer transition-all relative', selectedTemplate === 'classic' ? 'border-blue-500 shadow-lg' : 'border-gray-200 hover:border-blue-300']"
        >
          <div class="bg-white rounded-lg p-4 shadow-sm">
            <div class="h-32 bg-gradient-to-r from-blue-100 to-blue-50 rounded mb-3"></div>
            <div class="space-y-2">
              <div class="h-3 bg-gray-200 rounded w-3/4"></div>
              <div class="h-2 bg-gray-100 rounded w-1/2"></div>
              <div class="h-2 bg-gray-100 rounded w-2/3"></div>
            </div>
          </div>
          <span v-if="selectedTemplate === 'classic'" class="absolute top-2 right-2 bg-blue-500 text-white text-xs px-2 py-0.5 rounded-full">使用中</span>
          <p class="text-center text-sm font-medium text-gray-700 mt-3">经典模板</p>
        </div>
        <div
          @click="selectTemplate('simple')"
          :class="['border-2 rounded-xl p-4 cursor-pointer transition-all relative', selectedTemplate === 'simple' ? 'border-blue-500 shadow-lg' : 'border-gray-200 hover:border-blue-300']"
        >
          <div class="bg-white rounded-lg p-4 shadow-sm">
            <div class="h-32 bg-gradient-to-r from-green-100 to-green-50 rounded mb-3"></div>
            <div class="space-y-2">
              <div class="h-3 bg-gray-200 rounded w-3/4"></div>
              <div class="h-2 bg-gray-100 rounded w-1/2"></div>
              <div class="h-2 bg-gray-100 rounded w-2/3"></div>
            </div>
          </div>
          <span v-if="selectedTemplate === 'simple'" class="absolute top-2 right-2 bg-blue-500 text-white text-xs px-2 py-0.5 rounded-full">使用中</span>
          <p class="text-center text-sm font-medium text-gray-700 mt-3">简约模板</p>
        </div>
        <div
          @click="selectTemplate('tech')"
          :class="['border-2 rounded-xl p-4 cursor-pointer transition-all relative', selectedTemplate === 'tech' ? 'border-blue-500 shadow-lg' : 'border-gray-200 hover:border-blue-300']"
        >
          <div class="bg-white rounded-lg p-4 shadow-sm">
            <div class="h-32 bg-gradient-to-r from-purple-100 to-purple-50 rounded mb-3"></div>
            <div class="space-y-2">
              <div class="h-3 bg-gray-200 rounded w-3/4"></div>
              <div class="h-2 bg-gray-100 rounded w-1/2"></div>
              <div class="h-2 bg-gray-100 rounded w-2/3"></div>
            </div>
          </div>
          <span v-if="selectedTemplate === 'tech'" class="absolute top-2 right-2 bg-blue-500 text-white text-xs px-2 py-0.5 rounded-full">使用中</span>
          <p class="text-center text-sm font-medium text-gray-700 mt-3">技术岗模板</p>
        </div>
        <div
          @click="selectTemplate('design')"
          :class="['border-2 rounded-xl p-4 cursor-pointer transition-all relative', selectedTemplate === 'design' ? 'border-blue-500 shadow-lg' : 'border-gray-200 hover:border-blue-300']"
        >
          <div class="bg-white rounded-lg p-4 shadow-sm">
            <div class="h-32 bg-gradient-to-r from-orange-100 to-orange-50 rounded mb-3"></div>
            <div class="space-y-2">
              <div class="h-3 bg-gray-200 rounded w-3/4"></div>
              <div class="h-2 bg-gray-100 rounded w-1/2"></div>
              <div class="h-2 bg-gray-100 rounded w-2/3"></div>
            </div>
          </div>
          <span v-if="selectedTemplate === 'design'" class="absolute top-2 right-2 bg-blue-500 text-white text-xs px-2 py-0.5 rounded-full">使用中</span>
          <p class="text-center text-sm font-medium text-gray-700 mt-3">设计岗模板</p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-8">
      <div class="col-span-2 bg-white rounded-xl shadow-sm p-8" :class="{
        'template-classic': selectedTemplate === 'classic',
        'template-simple': selectedTemplate === 'simple',
        'template-tech': selectedTemplate === 'tech',
        'template-design': selectedTemplate === 'design'
      }" id="resume-content">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-bold text-gray-900">我的简历</h3>
          <div class="flex space-x-2">
            <button @click="previewResume" class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors">
              <i class="fas fa-eye mr-2"></i>预览
            </button>
          </div>
        </div>

        <div class="space-y-6">
          <div class="border-b border-gray-100 pb-6">
            <div class="flex items-center justify-between mb-4">
              <h4 class="font-bold text-gray-900 flex items-center">
                <i class="fas fa-user mr-2 text-blue-600"></i>基本信息
              </h4>
              <button @click="editSection('basic')" class="text-blue-600 hover:text-blue-700 text-sm">
                <i class="fas fa-edit mr-1"></i>编辑
              </button>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-500">姓名</p>
                <p class="font-medium text-gray-900">{{ resume.name }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">性别</p>
                <p class="font-medium text-gray-900">{{ resume.gender === 'male' ? '男' : '女' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">学历</p>
                <p class="font-medium text-gray-900">{{ educationLabel }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">专业</p>
                <p class="font-medium text-gray-900">{{ resume.major }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">手机</p>
                <p class="font-medium text-gray-900">{{ resume.phone }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">邮箱</p>
                <p class="font-medium text-gray-900">{{ resume.email }}</p>
              </div>
            </div>
          </div>

          <div class="border-b border-gray-100 pb-6">
            <div class="flex items-center justify-between mb-4">
              <h4 class="font-bold text-gray-900 flex items-center">
                <i class="fas fa-graduation-cap mr-2 text-blue-600"></i>教育经历
              </h4>
              <button @click="addEducation" class="text-blue-600 hover:text-blue-700 text-sm">
                <i class="fas fa-plus mr-1"></i>添加
              </button>
            </div>
            <div class="space-y-4">
              <div v-for="edu in resume.educationList" :key="edu.id" class="p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors">
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <p class="font-medium text-gray-900">{{ edu.school }}</p>
                    <p class="text-sm text-gray-600">{{ edu.major }} · {{ edu.degree }} · {{ edu.educationType }}</p>
                    <p class="text-xs text-gray-400 mt-1">{{ edu.startDate }} - {{ edu.endDate }}</p>
                    <p v-if="edu.courses" class="text-sm text-gray-500 mt-2">
                      <span class="font-medium">主修课程：</span>{{ edu.courses }}
                    </p>
                    <p v-if="edu.experience" class="text-sm text-gray-500 mt-1">
                      <span class="font-medium">在校经历：</span>{{ edu.experience }}
                    </p>
                  </div>
                  <div class="flex items-center gap-2">
                    <span :class="edu.isCurrent ? 'px-2 py-1 bg-blue-100 text-blue-700' : 'px-2 py-1 bg-green-100 text-green-700' + ' text-xs rounded'">
                      {{ edu.isCurrent ? '在读' : '已毕业' }}
                    </span>
                    <button @click="editEducation(edu)" class="text-gray-500 hover:text-blue-600 transition-colors">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="deleteEducation(edu.id)" class="text-gray-500 hover:text-red-600 transition-colors">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="border-b border-gray-100 pb-6">
            <div class="flex items-center justify-between mb-4">
              <h4 class="font-bold text-gray-900 flex items-center">
                <i class="fas fa-briefcase mr-2 text-blue-600"></i>实习/项目经历
              </h4>
              <button @click="addExperience" class="text-blue-600 hover:text-blue-700 text-sm">
                <i class="fas fa-plus mr-1"></i>添加
              </button>
            </div>
            <div v-if="resume.experienceList.length === 0" class="text-center py-8 text-gray-400">
              <i class="fas fa-briefcase text-4xl mb-2"></i>
              <p>暂无实习/项目经历</p>
            </div>
            <div v-else class="space-y-4">
              <div v-for="exp in resume.experienceList" :key="exp.id" class="p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors">
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <p class="font-medium text-gray-900">{{ exp.title }}</p>
                    <p class="text-xs text-gray-400">{{ exp.startDate }} - {{ exp.endDate }}</p>
                    <p class="text-sm text-gray-600 mt-2">{{ exp.description }}</p>
                  </div>
                  <div class="flex items-center gap-2">
                    <button @click="editExperience(exp)" class="text-gray-500 hover:text-blue-600 transition-colors">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="deleteExperience(exp.id)" class="text-gray-500 hover:text-red-600 transition-colors">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="border-b border-gray-100 pb-6">
            <div class="flex items-center justify-between mb-4">
              <h4 class="font-bold text-gray-900 flex items-center">
                <i class="fas fa-code mr-2 text-blue-600"></i>专业技能
              </h4>
              <button @click="editSection('skills')" class="text-blue-600 hover:text-blue-700 text-sm">
                <i class="fas fa-edit mr-1"></i>编辑
              </button>
            </div>
            <div class="flex flex-wrap gap-2">
              <span v-for="skill in resume.skillList" :key="skill" class="px-3 py-1.5 bg-blue-50 text-blue-700 text-sm rounded-full">
                {{ skill }}
              </span>
            </div>
          </div>

          <div class="pb-6">
            <div class="flex items-center justify-between mb-4">
              <h4 class="font-bold text-gray-900 flex items-center">
                <i class="fas fa-award mr-2 text-blue-600"></i>证书/荣誉
              </h4>
              <button @click="editSection('certificates')" class="text-blue-600 hover:text-blue-700 text-sm">
                <i class="fas fa-plus mr-1"></i>添加
              </button>
            </div>
            <div class="flex flex-wrap gap-3">
              <div v-for="cert in resume.certificateList" :key="cert.id" class="px-4 py-2 bg-gray-50 rounded-xl flex items-center gap-2">
                <div>
                  <p class="font-medium text-gray-900 text-sm">{{ cert.name }}</p>
                  <p v-if="cert.date" class="text-xs text-gray-400">{{ cert.date }}</p>
                  <p v-if="cert.description" class="text-xs text-gray-500 mt-1">{{ cert.description }}</p>
                </div>
                <button @click="deleteCertificate(cert.id)" class="text-gray-400 hover:text-red-600 transition-colors ml-2">
                  <i class="fas fa-times"></i>
                </button>
              </div>
              <div v-if="resume.certificateList.length === 0" class="text-center py-4 text-gray-400 w-full">
                <p>暂无证书/荣誉</p>
              </div>
            </div>
          </div>

          <div class="border-b border-gray-100 pb-6">
            <div class="flex items-center justify-between mb-4">
              <h4 class="font-bold text-gray-900 flex items-center">
                <i class="fas fa-star mr-2 text-blue-600"></i>个人优势
              </h4>
              <button @click="editSection('strengths')" class="text-blue-600 hover:text-blue-700 text-sm">
                <i class="fas fa-edit mr-1"></i>编辑
              </button>
            </div>
            <div v-if="resume.strengths" class="text-gray-700 whitespace-pre-wrap">
              {{ resume.strengths }}
            </div>
            <div v-else class="text-gray-400 text-sm">
              点击编辑添加个人优势
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div class="bg-white rounded-xl shadow-sm p-6">
          <h3 class="font-bold text-gray-900 mb-4">简历完整度</h3>
          <div class="relative pt-1">
            <div class="flex mb-2 items-center justify-between">
              <div>
                <span class="text-xs font-semibold inline-block text-blue-600">{{ completeness }}%</span>
              </div>
            </div>
            <div class="overflow-hidden h-2 text-xs flex rounded-full bg-blue-100">
              <div :style="{ width: completeness + '%' }" class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-blue-600"></div>
            </div>
          </div>
          <p class="text-sm text-gray-500 mt-2">完善以下内容可提升竞争力</p>
          <div class="mt-4 space-y-2">
            <div v-for="item in completenessItems" :key="item.name" class="flex items-center text-sm">
              <i :class="item.done ? 'fas fa-check-circle text-green-500' : 'far fa-circle'" class="mr-2"></i>
              <span :class="item.done ? 'text-gray-600' : 'text-gray-400'">{{ item.name }}</span>
            </div>
          </div>
        </div>

        <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
          <h3 class="font-bold text-gray-900 mb-4 flex items-center justify-between">
            <span><i class="fas fa-lightbulb mr-2 text-yellow-500"></i>优化建议</span>
            <button v-if="suggestions.length > 0" @click="fetchSuggestions" class="text-gray-400 hover:text-blue-600 transition-colors" title="刷新建议">
              <i class="fas fa-sync-alt" :class="{'fa-spin': suggestionsLoading}"></i>
            </button>
          </h3>
          <div v-if="suggestionsLoading" class="flex items-center justify-center py-4">
            <i class="fas fa-spinner fa-spin text-blue-500 mr-2"></i>
            <span class="text-gray-500">AI分析中...</span>
          </div>
          <div v-else-if="suggestions.length > 0" class="space-y-3">
            <div v-for="(suggestion, index) in suggestions" :key="index" class="flex items-start space-x-2">
              <i class="fas fa-arrow-right text-blue-500 mt-1"></i>
              <p class="text-sm text-gray-600">{{ suggestion }}</p>
            </div>
          </div>
          <div v-else class="space-y-3">
            <div class="flex items-start space-x-2">
              <i class="fas fa-arrow-right text-blue-500 mt-1"></i>
              <p class="text-sm text-gray-600">建议完善简历信息以获得更准确的建议</p>
            </div>
            <button @click="fetchSuggestions" class="w-full py-2 bg-blue-50 hover:bg-blue-100 text-blue-600 rounded-lg transition-colors text-sm">
              <i class="fas fa-robot mr-1"></i>获取AI建议
            </button>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm p-6">
          <h3 class="font-bold text-gray-900 mb-4">快捷操作</h3>
          <div class="space-y-3">
            <input type="file" ref="fileInput" @change="handleFileUpload" accept=".pdf" class="hidden" />
            <button @click="triggerFileUpload" :disabled="uploadLoading" class="w-full py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors flex items-center justify-center space-x-2 disabled:opacity-50">
              <i v-if="uploadLoading" class="fas fa-spinner fa-spin"></i>
              <i v-else class="fas fa-upload"></i>
              <span>{{ uploadLoading ? '上传中...' : '上传附件简历' }}</span>
            </button>
            <a v-if="resume.attachment_url" :href="'http://localhost:8000' + resume.attachment_url" target="_blank" class="w-full py-2.5 bg-blue-50 hover:bg-blue-100 text-blue-600 rounded-lg transition-colors flex items-center justify-center space-x-2">
              <i class="fas fa-eye"></i>
              <span>查看附件</span>
            </a>
            <button @click="exportToPDF" class="w-full py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors flex items-center justify-center space-x-2">
              <i class="fas fa-download"></i>
              <span>导出PDF</span>
            </button>
            <button @click="copyLink" class="w-full py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors flex items-center justify-center space-x-2">
              <i class="fas fa-copy"></i>
              <span>复制简历链接</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <el-dialog
      v-model="showEditDialog"
      :title="editTitle"
      width="550px"
      :close-on-click-modal="false"
      class="resume-edit-dialog"
    >
      <el-form :model="editForm" label-position="top" class="edit-form" v-if="editSectionName === 'basic' || editSectionName === 'skills'">
        <el-form-item v-if="editSectionName === 'basic'" label="姓名">
          <el-input v-model="editForm.name" placeholder="请输入姓名" size="large" />
        </el-form-item>
        <el-form-item v-if="editSectionName === 'basic'" label="性别">
          <el-select v-model="editForm.gender" class="w-full" placeholder="请选择性别" size="large">
            <el-option label="男" value="male" />
            <el-option label="女" value="female" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="editSectionName === 'basic'" label="手机号">
          <el-input v-model="editForm.phone" placeholder="请输入手机号" size="large" />
        </el-form-item>
        <el-form-item v-if="editSectionName === 'basic'" label="邮箱">
          <el-input v-model="editForm.email" placeholder="请输入邮箱" size="large" />
        </el-form-item>
        <el-form-item v-if="editSectionName === 'basic'" label="专业">
          <el-input v-model="editForm.major" placeholder="请输入专业" size="large" />
        </el-form-item>
        <el-form-item v-if="editSectionName === 'basic'" label="学历">
          <el-select v-model="editForm.education" class="w-full" placeholder="请选择学历" size="large">
            <el-option label="本科" value="bachelor" />
            <el-option label="硕士" value="master" />
            <el-option label="博士" value="doctor" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="editSectionName === 'skills'" label="专业技能">
          <el-input
            v-model="editForm.skills"
            type="textarea"
            :rows="4"
            placeholder="请输入技能，多个技能用逗号分隔，如：Python, Vue.js, MySQL"
          />
        </el-form-item>
      </el-form>

      <el-form :model="educationForm" label-position="top" class="edit-form" v-if="editSectionName === 'education'">
        <el-form-item label="学校名称" class="is-required">
          <el-autocomplete
            v-model="educationForm.school"
            :fetch-suggestions="universityQuery"
            placeholder="请输入学校名称"
            size="large"
            class="w-full"
            :trigger-on-focus="false"
            highlight-first-item
            @select="handleUniversitySelect"
          >
            <template #prefix>
              <i class="el-icon-search"></i>
            </template>
            <template #default="{ item }">
              <div class="university-item">
                <span class="university-name">{{ item.name }}</span>
                <span class="university-info">{{ item.province }} · {{ item.type }}</span>
              </div>
            </template>
          </el-autocomplete>
        </el-form-item>
        <el-form-item label="专业" class="is-required">
          <el-autocomplete
            v-model="educationForm.major"
            :fetch-suggestions="majorQuery"
            placeholder="请输入专业"
            size="large"
            class="w-full"
            :trigger-on-focus="false"
            highlight-first-item
            @select="handleMajorSelect"
          >
            <template #prefix>
              <i class="el-icon-search"></i>
            </template>
            <template #default="{ item }">
              <div class="university-item">
                <span class="university-name">{{ item.name }}</span>
                <span class="university-info">{{ item.category }} · {{ item.type }}</span>
              </div>
            </template>
          </el-autocomplete>
        </el-form-item>
        <el-form-item label="学历" class="is-required">
          <div class="degree-scroll-container">
            <div class="degree-scroll-wrapper">
              <div
                v-for="(item, index) in degreeOptions"
                :key="index"
                :class="['degree-item', { active: selectedDegreeIndex === index }]"
                @click="selectDegree(index)"
              >
                <span class="degree-value">{{ item.value }}</span>
                <span class="degree-label">{{ item.label }}</span>
              </div>
            </div>
            <div class="degree-indicator">
              <div class="degree-track">
                <div
                  class="degree-track-fill"
                  :style="{ width: ((selectedDegreeIndex + 1) / degreeOptions.length * 100) + '%' }"
                ></div>
              </div>
              <div class="degree-dots">
                <span
                  v-for="(item, index) in degreeOptions"
                  :key="index"
                  :class="['degree-dot', { active: selectedDegreeIndex >= index }]"
                ></span>
              </div>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="学习形式" class="is-required">
          <el-radio-group v-model="educationForm.educationType" size="large">
            <el-radio label="全日制" border />
            <el-radio label="非全日制" border />
          </el-radio-group>
        </el-form-item>
        <el-form-item label="入学时间" class="is-required">
          <el-date-picker
            v-model="educationForm.startDate"
            type="month"
            placeholder="选择入学时间"
            class="w-full"
            size="large"
            format="YYYY/MM"
            value-format="YYYY/MM"
          />
        </el-form-item>
        <el-form-item label="毕业时间">
          <el-date-picker
            v-model="educationForm.endDate"
            type="month"
            placeholder="选择毕业时间"
            class="w-full"
            size="large"
            format="YYYY/MM"
            value-format="YYYY/MM"
            :disabled="educationForm.isCurrent"
          />
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="educationForm.isCurrent">目前在读</el-checkbox>
        </el-form-item>
        <el-form-item label="主修课程">
          <el-input
            v-model="educationForm.courses"
            type="textarea"
            :rows="2"
            placeholder="请输入主修课程，如：数据结构、算法设计、操作系统"
            size="large"
          />
        </el-form-item>
        <el-form-item label="在校经历">
          <el-input
            v-model="educationForm.experience"
            type="textarea"
            :rows="3"
            placeholder="请输入在校经历，如：担任学生会干部、志愿者活动、竞赛获奖等"
            size="large"
          />
        </el-form-item>
      </el-form>
      <el-form :model="experienceForm" label-position="top" class="edit-form" v-if="editSectionName === 'experience'">
        <el-form-item label="经历名称" class="is-required">
          <el-input
            v-model="experienceForm.title"
            placeholder="如：后端开发实习生 · 字节跳动"
            size="large"
          />
        </el-form-item>
        <el-form-item label="开始时间" class="is-required">
          <el-date-picker
            v-model="experienceForm.startDate"
            type="month"
            placeholder="选择开始时间"
            class="w-full"
            size="large"
            format="YYYY/MM"
            value-format="YYYY/MM"
          />
        </el-form-item>
        <el-form-item label="结束时间">
          <el-date-picker
            v-model="experienceForm.endDate"
            type="month"
            placeholder="选择结束时间"
            class="w-full"
            size="large"
            format="YYYY/MM"
            value-format="YYYY/MM"
            :disabled="experienceForm.isCurrent"
          />
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="experienceForm.isCurrent">目前在职</el-checkbox>
        </el-form-item>
        <el-form-item label="经历描述">
          <el-input
            v-model="experienceForm.description"
            type="textarea"
            :rows="4"
            placeholder="请描述工作内容、成果等"
            size="large"
          />
        </el-form-item>
      </el-form>
      <el-form :model="certificateForm" label-position="top" class="edit-form" v-if="editSectionName === 'certificates'">
        <el-form-item label="证书名称" class="is-required">
          <el-input
            v-model="certificateForm.name"
            placeholder="请输入证书名称，如：计算机二级、英语六级"
            size="large"
          />
        </el-form-item>
        <el-form-item label="获得时间">
          <el-date-picker
            v-model="certificateForm.date"
            type="month"
            placeholder="选择获得时间"
            class="w-full"
            size="large"
            format="YYYY/MM"
            value-format="YYYY/MM"
          />
        </el-form-item>
        <el-form-item label="证书描述">
          <el-input
            v-model="certificateForm.description"
            type="textarea"
            :rows="3"
            placeholder="请描述证书详情，如：成绩、排名等"
            size="large"
          />
        </el-form-item>
      </el-form>
      <el-form :model="editForm" label-position="top" class="edit-form" v-if="editSectionName === 'strengths'">
        <el-form-item label="个人优势">
          <el-input
            v-model="editForm.strengths"
            type="textarea"
            :rows="6"
            placeholder="请输入个人优势，如：技术能力、沟通能力、团队协作等"
            size="large"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showEditDialog = false" size="large">取消</el-button>
          <el-button v-if="editSectionName === 'education'" type="primary" @click="saveEducation" size="large">保存</el-button>
          <el-button v-else-if="editSectionName === 'experience'" type="primary" @click="saveExperience" size="large">保存</el-button>
          <el-button v-else-if="editSectionName === 'certificates'" type="primary" @click="saveCertificate" size="large">保存</el-button>
          <el-button v-else type="primary" @click="saveEdit" size="large">保存</el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog
      v-model="showPreviewDialog"
      title="简历预览"
      width="800px"
      :close-on-click-modal="true"
    >
      <div class="preview-container" ref="previewContainer">
        <iframe :src="previewPdfUrl" class="pdf-iframe" v-if="previewPdfUrl"></iframe>
        <div v-else class="no-preview">暂无PDF预览</div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { searchUniversities } from '@/data/universities'
import { searchMajors } from '@/data/majors'
import { studentAPI } from '@/api'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'

const resume = reactive({
  id: null,
  title: '我的简历',
  visibility: 'public',
  template: 'default',
  name: '',
  gender: '',
  phone: '',
  email: '',
  school: '',
  major: '',
  education: '',
  graduationYear: '',
  educationList: [],
  experienceList: [],
  skillList: [],
  certificateList: [],
  selfEvaluation: '',
  strengths: '',
  attachment_url: ''
})

const loading = ref(false)
const suggestions = ref([])
const suggestionsLoading = ref(false)
const fileInput = ref(null)
const uploadLoading = ref(false)
const showPreviewDialog = ref(false)
const previewPdfUrl = ref('')
const previewContainer = ref(null)

onMounted(async () => {
  await loadResume()
})

const loadResume = async () => {
  try {
    loading.value = true
    const profileRes = await studentAPI.getProfile()
    const profileData = profileRes?.data?.data || profileRes?.data
    if (profileData) {
      resume.name = profileData.name || ''
      resume.gender = profileData.gender || ''
      resume.phone = profileData.phone || ''
      resume.major = profileData.major || ''
    }
    const res = await studentAPI.getResumes()
    const resumeData = res?.data?.data || res?.data
    if (resumeData && resumeData.length > 0) {
      const data = resumeData[0]
      resume.id = data.id
      resume.title = data.title || '我的简历'
      resume.visibility = data.visibility || 'public'
      resume.template = data.template || 'default'
      resume.email = data.personal_email || ''
      resume.school = data.education_school || ''
      if (data.education_major) resume.major = data.education_major
      resume.education = data.education_degree || ''
      resume.graduationYear = data.education_end || ''
      resume.selfEvaluation = data.self_evaluation || ''
      resume.strengths = data.strengths || ''
      resume.attachment_url = data.attachment_url || ''
      resume.skillList = data.skill_names ? data.skill_names.split(',').map(s => s.trim()) : []
      resume.certificateList = data.certificate_names ? data.certificate_names.split(',').map(s => s.trim()) : []
      if (data.certificate_list) {
        try {
          const parsed = JSON.parse(data.certificate_list)
          if (Array.isArray(parsed) && parsed.length > 0 && typeof parsed[0] === 'object') {
            resume.certificateList = parsed
          }
        } catch (e) {
        }
      }
      if (data.education_list) {
        try {
          resume.educationList = JSON.parse(data.education_list)
        } catch (e) {
          resume.educationList = []
        }
      }
      if (data.experience_list) {
        try {
          resume.experienceList = JSON.parse(data.experience_list)
        } catch (e) {
          resume.experienceList = []
        }
      }
    }
  } catch (error) {
    console.error('加载简历失败:', error)
  } finally {
    loading.value = false
  }
}

const fetchSuggestions = async () => {
  if (!resume.id) return
  try {
    suggestionsLoading.value = true
    const res = await studentAPI.getResumeSuggestions(resume.id)
    suggestions.value = res.data?.suggestions || res.data || []
  } catch (error) {
    console.error('获取建议失败:', error)
    suggestions.value = []
  } finally {
    suggestionsLoading.value = false
  }
}

const completenessItems = reactive([
  { name: '基本信息', done: false },
  { name: '教育经历', done: false },
  { name: '实习/项目经历', done: false },
  { name: '专业技能', done: false },
  { name: '证书/荣誉', done: false },
  { name: '个人优势', done: false }
])

const updateCompleteness = () => {
  completenessItems[0].done = !!resume.name && !!resume.phone && !!resume.email
  completenessItems[1].done = resume.educationList.length > 0
  completenessItems[2].done = resume.experienceList.length > 0
  completenessItems[3].done = resume.skillList.length > 0
  completenessItems[4].done = resume.certificateList.length > 0
  completenessItems[5].done = !!resume.strengths
}

watch(() => resume.name, updateCompleteness, { immediate: true })
watch(() => resume.phone, updateCompleteness, { immediate: true })
watch(() => resume.email, updateCompleteness, { immediate: true })
watch(() => resume.educationList.length, updateCompleteness, { immediate: true })
watch(() => resume.experienceList.length, updateCompleteness, { immediate: true })
watch(() => resume.skillList.length, updateCompleteness, { immediate: true })
watch(() => resume.certificateList.length, updateCompleteness, { immediate: true })
watch(() => resume.strengths, updateCompleteness, { immediate: true })

const completeness = computed(() => {
  const done = completenessItems.filter(item => item.done).length
  return Math.round((done / completenessItems.length) * 100)
})

const educationLabel = computed(() => {
  const labels = { bachelor: '本科', master: '硕士', doctor: '博士' }
  return labels[resume.education] || '本科'
})

const degreeOptions = [
  { label: '专科', value: '专科' },
  { label: '本科', value: '本科' },
  { label: '硕士', value: '硕士' },
  { label: '博士', value: '博士' }
]

const selectedDegreeIndex = ref(1)

const selectedTemplate = ref('classic')

const selectTemplate = (template) => {
  selectedTemplate.value = template
}

const selectDegree = (index) => {
  selectedDegreeIndex.value = index
  educationForm.degree = degreeOptions[index].value
}

const universityQuery = (query) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(searchUniversities(query))
    }, 100)
  })
}

const handleUniversitySelect = (item) => {
  educationForm.school = item.name
}

const majorQuery = (query) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(searchMajors(query))
    }, 100)
  })
}

const handleMajorSelect = (item) => {
  educationForm.major = item.name
}

const showEditDialog = ref(false)
const editSectionName = ref('')
const editTitle = ref('')
const editForm = reactive({
  name: '',
  gender: '',
  phone: '',
  email: '',
  major: '',
  education: '',
  skills: '',
  strengths: ''
})

const educationForm = reactive({
  id: null,
  school: '',
  major: '',
  degree: '',
  educationType: '全日制',
  startDate: '',
  endDate: '',
  isCurrent: false,
  courses: '',
  experience: ''
})

const experienceForm = reactive({
  id: null,
  title: '',
  startDate: '',
  endDate: '',
  description: '',
  isCurrent: false
})

const certificateForm = reactive({
  name: '',
  date: '',
  description: ''
})

const isEditingEducation = ref(false)
const isEditingExperience = ref(false)
const isEditingCertificate = ref(false)

const editSection = (section) => {
  editSectionName.value = section
  if (section === 'basic') {
    editTitle.value = '编辑基本信息'
    editForm.name = resume.name
    editForm.gender = resume.gender
    editForm.phone = resume.phone
    editForm.email = resume.email
    editForm.major = resume.major
    editForm.education = resume.education
  } else if (section === 'skills') {
    editTitle.value = '编辑专业技能'
    editForm.skills = resume.skillList.join(', ')
  } else if (section === 'certificates') {
    editTitle.value = '添加证书/荣誉'
    isEditingCertificate.value = false
    certificateForm.name = ''
    certificateForm.date = ''
    certificateForm.description = ''
  } else if (section === 'strengths') {
    editTitle.value = '编辑个人优势'
    editForm.strengths = resume.strengths || ''
  }
  showEditDialog.value = true
}

const addEducation = () => {
  editSectionName.value = 'education'
  editTitle.value = '添加教育经历'
  isEditingEducation.value = false
  educationForm.id = null
  educationForm.school = ''
  educationForm.major = ''
  selectedDegreeIndex.value = 1
  educationForm.degree = '本科'
  educationForm.educationType = '全日制'
  educationForm.startDate = ''
  educationForm.endDate = ''
  educationForm.isCurrent = false
  educationForm.courses = ''
  educationForm.experience = ''
  showEditDialog.value = true
}

const editEducation = (edu) => {
  editSectionName.value = 'education'
  editTitle.value = '编辑教育经历'
  isEditingEducation.value = true
  educationForm.id = edu.id
  educationForm.school = edu.school
  educationForm.major = edu.major
  const degreeIndex = degreeOptions.findIndex(d => d.value === edu.degree)
  selectedDegreeIndex.value = degreeIndex >= 0 ? degreeIndex : 1
  educationForm.degree = edu.degree || '本科'
  educationForm.startDate = edu.startDate
  educationForm.endDate = edu.endDate
  educationForm.isCurrent = edu.isCurrent
  educationForm.educationType = edu.educationType || '全日制'
  educationForm.courses = edu.courses || ''
  educationForm.experience = edu.experience || ''
  showEditDialog.value = true
}

const deleteEducation = async (eduId) => {
  const index = resume.educationList.findIndex(e => e.id === eduId)
  if (index > -1) {
    resume.educationList.splice(index, 1)
    ElMessage.success('删除成功')
    await saveResume()
  }
}

const saveEducation = async () => {
  if (!educationForm.school || !educationForm.major || !educationForm.degree || !educationForm.startDate) {
    ElMessage.warning('请填写完整信息')
    return
  }

  if (isEditingEducation.value) {
    const index = resume.educationList.findIndex(e => e.id === educationForm.id)
    if (index > -1) {
      resume.educationList[index] = {
        ...educationForm,
        endDate: educationForm.isCurrent ? '至今' : educationForm.endDate
      }
    }
    ElMessage.success('更新成功')
    showEditDialog.value = false
    updateCompleteness()
    await saveResume()
  } else {
    const newEdu = {
      id: Date.now(),
      school: educationForm.school,
      major: educationForm.major,
      degree: educationForm.degree,
      educationType: educationForm.educationType,
      startDate: educationForm.startDate,
      endDate: educationForm.isCurrent ? '至今' : educationForm.endDate,
      isCurrent: educationForm.isCurrent,
      courses: educationForm.courses,
      experience: educationForm.experience
    }
    resume.educationList.unshift(newEdu)
    ElMessage.success('添加成功')
    showEditDialog.value = false
    updateCompleteness()
    await saveResume()
  }
}

const addExperience = () => {
  editSectionName.value = 'experience'
  editTitle.value = '添加实习/项目经历'
  isEditingExperience.value = false
  experienceForm.id = null
  experienceForm.title = ''
  experienceForm.startDate = ''
  experienceForm.endDate = ''
  experienceForm.description = ''
  experienceForm.isCurrent = false
  showEditDialog.value = true
}

const editExperience = (exp) => {
  editSectionName.value = 'experience'
  editTitle.value = '编辑实习/项目经历'
  isEditingExperience.value = true
  experienceForm.id = exp.id
  experienceForm.title = exp.title
  experienceForm.startDate = exp.startDate
  experienceForm.endDate = exp.endDate === '至今' ? '' : exp.endDate
  experienceForm.description = exp.description
  experienceForm.isCurrent = exp.endDate === '至今'
  showEditDialog.value = true
}

const deleteExperience = async (expId) => {
  const index = resume.experienceList.findIndex(e => e.id === expId)
  if (index > -1) {
    resume.experienceList.splice(index, 1)
    ElMessage.success('删除成功')
    updateCompleteness()
    await saveResume()
  }
}

const saveExperience = async () => {
  if (!experienceForm.title || !experienceForm.startDate) {
    ElMessage.warning('请填写完整信息')
    return
  }

  if (isEditingExperience.value) {
    const index = resume.experienceList.findIndex(e => e.id === experienceForm.id)
    if (index > -1) {
      resume.experienceList[index] = {
        ...experienceForm,
        endDate: experienceForm.isCurrent ? '至今' : experienceForm.endDate
      }
    }
    ElMessage.success('更新成功')
    showEditDialog.value = false
    updateCompleteness()
    await saveResume()
  } else {
    const newExp = {
      id: Date.now(),
      title: experienceForm.title,
      startDate: experienceForm.startDate,
      endDate: experienceForm.isCurrent ? '至今' : experienceForm.endDate,
      description: experienceForm.description
    }
    resume.experienceList.unshift(newExp)
    ElMessage.success('添加成功')
    showEditDialog.value = false
    updateCompleteness()
    await saveResume()
  }
}

const saveCertificate = async () => {
  if (!certificateForm.name) {
    ElMessage.warning('请输入证书名称')
    return
  }

  const newCert = {
    id: Date.now(),
    name: certificateForm.name,
    date: certificateForm.date || '',
    description: certificateForm.description || ''
  }
  resume.certificateList.push(newCert)
  ElMessage.success('添加成功')
  showEditDialog.value = false
  updateCompleteness()
  await saveResume()
}

const deleteCertificate = async (certId) => {
  const index = resume.certificateList.findIndex(c => c.id === certId)
  if (index > -1) {
    resume.certificateList.splice(index, 1)
    ElMessage.success('删除成功')
    await saveResume()
  }
}

const saveEdit = async () => {
  if (editSectionName.value === 'basic') {
    resume.name = editForm.name
    resume.gender = editForm.gender
    resume.phone = editForm.phone
    resume.email = editForm.email
    resume.major = editForm.major
    resume.education = editForm.education
  } else if (editSectionName.value === 'skills') {
    resume.skillList = editForm.skills.split(',').map(s => s.trim()).filter(s => s)
  } else if (editSectionName.value === 'strengths') {
    resume.strengths = editForm.strengths
  }
  showEditDialog.value = false
  ElMessage.success('保存成功')
  await saveResume()
}

const saveResume = async () => {
  try {
    loading.value = true
    const data = {
      title: resume.title || '我的简历',
      visibility: resume.visibility || 'public',
      template: resume.template || 'default',
      personal_name: resume.name || '',
      personal_gender: resume.gender || '',
      personal_phone: resume.phone || '',
      personal_email: resume.email || null,
      education_school: resume.educationList.length > 0 ? resume.educationList[0].school : null,
      education_major: resume.educationList.length > 0 ? resume.educationList[0].major : null,
      education_degree: resume.educationList.length > 0 ? resume.educationList[0].degree : null,
      education_start: resume.educationList.length > 0 ? resume.educationList[0].startDate : null,
      education_end: resume.educationList.length > 0 ? resume.educationList[0].endDate : null,
      experience_company: resume.experienceList.length > 0 ? resume.experienceList[0].title : null,
      experience_position: resume.experienceList.length > 0 ? resume.experienceList[0].title : null,
      experience_duration: resume.experienceList.length > 0 ? `${resume.experienceList[0].startDate} - ${resume.experienceList[0].endDate}` : null,
      experience_description: resume.experienceList.length > 0 ? resume.experienceList[0].description : null,
      skill_names: resume.skillList.length > 0 ? resume.skillList.join(',') : null,
      certificate_names: resume.certificateList.length > 0 ? resume.certificateList.map(c => c.name).join(',') : null,
      self_evaluation: resume.selfEvaluation || null,
      strengths: resume.strengths || null,
      education_list: JSON.stringify(resume.educationList),
      experience_list: JSON.stringify(resume.experienceList),
      certificate_list: JSON.stringify(resume.certificateList)
    }
    if (resume.id) {
      const res = await studentAPI.updateResume(resume.id, data)
    } else {
      const res = await studentAPI.createResume(data)
      if (res.data && res.data.id) {
        resume.id = res.data.id
      }
    }
    ElMessage.success('简历保存成功')
  } catch (error) {
    console.error('保存简历失败:', error)
    ElMessage.error(error.response?.data?.detail || error.message || '保存失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const previewResume = async () => {
  const element = document.getElementById('resume-content')
  if (!element) {
    ElMessage.error('无法找到简历内容')
    return
  }

  const editButtons = element.querySelectorAll('button')
  editButtons.forEach(btn => btn.style.display = 'none')

  try {
    ElMessage.info('正在生成预览...')
    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
      logging: false,
      backgroundColor: '#ffffff'
    })

    const imgData = canvas.toDataURL('image/png')
    const pdf = new jsPDF('p', 'mm', 'a4')
    const imgWidth = 210
    const pageHeight = 297
    const imgHeight = (canvas.height * imgWidth) / canvas.width

    let heightLeft = imgHeight
    let position = 0

    pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
    heightLeft -= pageHeight

    while (heightLeft >= 0) {
      position = heightLeft - imgHeight
      pdf.addPage()
      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
      heightLeft -= pageHeight
    }

    previewPdfUrl.value = pdf.output('bloburl')
    showPreviewDialog.value = true
  } catch (error) {
    console.error('Preview error:', error)
    ElMessage.error('预览生成失败')
  } finally {
    editButtons.forEach(btn => btn.style.display = '')
  }
}

const copyLink = () => {
  ElMessage.success('简历链接已复制')
}

const exportToPDF = async () => {
  const element = document.getElementById('resume-content')
  if (!element) {
    ElMessage.error('无法找到简历内容')
    return
  }

  const editButtons = element.querySelectorAll('button')
  editButtons.forEach(btn => btn.style.display = 'none')

  try {
    ElMessage.info('正在生成PDF...')
    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
      logging: false,
      backgroundColor: '#ffffff'
    })

    const imgData = canvas.toDataURL('image/png')
    const pdf = new jsPDF('p', 'mm', 'a4')
    const imgWidth = 210
    const pageHeight = 297
    const imgHeight = (canvas.height * imgWidth) / canvas.width

    let heightLeft = imgHeight
    let position = 0

    pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
    heightLeft -= pageHeight

    while (heightLeft >= 0) {
      position = heightLeft - imgHeight
      pdf.addPage()
      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
      heightLeft -= pageHeight
    }

    pdf.save('我的简历.pdf')
    ElMessage.success('PDF导出成功')
  } catch (error) {
    console.error('PDF export error:', error)
    ElMessage.error('PDF导出失败')
  } finally {
    editButtons.forEach(btn => btn.style.display = '')
  }
}

const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.name.toLowerCase().endsWith('.pdf')) {
    ElMessage.error('仅支持 PDF 格式文件')
    return
  }

  if (file.size > 10 * 1024 * 1024) {
    ElMessage.error('文件大小不能超过 10MB')
    return
  }

  try {
    uploadLoading.value = true
    const formData = new FormData()
    formData.append('file', file)
    if (resume.id) {
      formData.append('resume_id', resume.id)
    }

    const response = await studentAPI.uploadResume(formData)
    if (response.data?.url || response.data?.data?.url) {
      resume.attachment_url = response.data.url || response.data.data.url
      ElMessage.success('简历上传成功')
    } else {
      ElMessage.success('简历上传成功')
    }
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('上传失败，请重试')
  } finally {
    uploadLoading.value = false
    event.target.value = ''
  }
}
</script>

<style scoped>
.edit-form :deep(.el-form-item__label) {
  font-weight: 600;
  color: #374151;
  padding-bottom: 8px;
  font-size: 14px;
}

.edit-form :deep(.el-form-item.is-required .el-form-item__label::before) {
  content: '*';
  color: #ef4444;
  margin-right: 4px;
  font-weight: 600;
}

.edit-form :deep(.el-input__wrapper),
.edit-form :deep(.el-textarea__inner) {
  border-radius: 10px;
  padding: 12px 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.edit-form :deep(.el-input__wrapper:hover),
.edit-form :deep(.el-textarea__inner:hover) {
  border-color: #93c5fd;
}

.edit-form :deep(.el-input__wrapper.is-focus),
.edit-form :deep(.el-textarea__inner:focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.edit-form :deep(.el-select) {
  width: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.dialog-footer .el-button {
  border-radius: 10px;
  padding: 12px 24px;
  font-weight: 500;
}

.dialog-footer .el-button--primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border: none;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.dialog-footer .el-button--primary:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  transform: translateY(-1px);
}

:deep(.el-dialog) {
  border-radius: 16px;
  overflow: hidden;
}

:deep(.el-dialog__header) {
  padding: 20px 24px;
  border-bottom: 1px solid #f3f4f6;
  margin-right: 0;
}

:deep(.el-dialog__title) {
  font-weight: 700;
  font-size: 18px;
  color: #111827;
}

:deep(.el-dialog__body) {
  padding: 24px;
}

:deep(.el-dialog__footer) {
  padding: 16px 24px 20px;
  border-top: 1px solid #f3f4f6;
}

.edit-form :deep(.el-autocomplete) {
  width: 100%;
}

.edit-form :deep(.el-autocomplete .el-input__wrapper) {
  border-radius: 10px;
  padding: 12px 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.edit-form :deep(.el-autocomplete .el-input__wrapper:hover) {
  border-color: #93c5fd;
}

.edit-form :deep(.el-autocomplete .el-input__wrapper.is-focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.university-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.university-name {
  font-weight: 500;
  color: #374151;
}

.university-info {
  font-size: 12px;
  color: #9ca3af;
}

:deep(.el-autocomplete-suggestion__wrap) {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

:deep(.el-autocomplete-suggestion__li) {
  padding: 10px 16px;
  border-bottom: 1px solid #f3f4f6;
}

:deep(.el-autocomplete-suggestion__li:last-child) {
  border-bottom: none;
}

:deep(.el-autocomplete-suggestion__li:hover) {
  background-color: #f9fafb;
}

.edit-form :deep(.el-slider__marks-text) {
  font-size: 12px;
  color: #6b7280;
  margin-top: 8px;
}

.education-degree-selector {
  padding: 30px 8px 10px;
  position: relative;
}

.edit-form :deep(.el-slider__marks) {
  top: 20px;
}

.edit-form :deep(.el-radio-group) {
  display: flex;
  gap: 12px;
}

.edit-form :deep(.el-radio--border) {
  border-radius: 8px;
  padding: 8px 16px;
  margin: 0;
}

.edit-form :deep(.el-radio.is-checked.is-border) {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-color: #3b82f6;
}

.edit-form :deep(.el-radio.is-checked.is-border .el-radio__label) {
  color: white;
}

.degree-scroll-container {
  padding: 10px 0;
}

.degree-scroll-wrapper {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding: 10px 5px;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
}

.degree-scroll-wrapper::-webkit-scrollbar {
  display: none;
}

.degree-item {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: #f3f4f6;
  cursor: pointer;
  transition: all 0.3s ease;
  scroll-snap-align: center;
  border: 2px solid transparent;
}

.degree-item:hover {
  background: #e5e7eb;
  transform: translateY(-2px);
}

.degree-item.active {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  transform: translateY(-2px);
}

.degree-item.active .degree-value,
.degree-item.active .degree-label {
  color: white;
}

.degree-value {
  font-size: 18px;
  font-weight: 700;
  color: #374151;
  margin-bottom: 4px;
}

.degree-label {
  font-size: 11px;
  color: #6b7280;
}

.degree-indicator {
  margin-top: 12px;
  position: relative;
}

.degree-track {
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
}

.degree-track-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.degree-dots {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  transform: translateY(-50%);
  pointer-events: none;
}

.degree-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #d1d5db;
  transition: all 0.3s ease;
}

.degree-dot.active {
  background: #3b82f6;
  transform: scale(1.2);
}

.preview-container {
  width: 100%;
  height: 600px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
}

.pdf-iframe {
  width: 100%;
  height: 100%;
  border: none;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.no-preview {
  color: #999;
  font-size: 14px;
}

.template-classic {
  font-family: 'SimSun', serif;
}

.template-simple {
  font-family: 'Arial', sans-serif;
  background: #fafafa;
}

.template-simple .border-b {
  border-color: #e0e0e0;
}

.template-tech {
  font-family: 'Consolas', monospace;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.template-tech .border-b {
  border-color: rgba(255, 255, 255, 0.2);
}

.template-tech h4,
.template-tech p,
.template-tech .text-gray-900,
.template-tech .text-gray-500,
.template-tech .text-gray-600,
.template-tech .text-gray-700,
.template-tech button {
  color: white !important;
}

.template-tech button.text-blue-600 {
  color: #fbbf24 !important;
}

.template-tech .space-y-3 button {
  background: rgba(255, 255, 255, 0.15) !important;
  color: white !important;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.template-tech .space-y-3 button:hover {
  background: rgba(255, 255, 255, 0.25) !important;
}

.template-design h4,
.template-design p,
.template-design .text-gray-900,
.template-design .text-gray-500,
.template-design .text-gray-600,
.template-design .text-gray-700,
.template-design button {
  color: white !important;
}

.template-design button.text-blue-600 {
  color: #fde68a !important;
}

.template-design .space-y-3 button {
  background: rgba(255, 255, 255, 0.15) !important;
  color: white !important;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.template-design .space-y-3 button:hover {
  background: rgba(255, 255, 255, 0.25) !important;
}

.template-design {
  font-family: 'Georgia', serif;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-radius: 20px;
}

.template-design .border-b {
  border-color: rgba(255, 255, 255, 0.3);
}

.template-design h4,
.template-design p,
.template-design .text-gray-900,
.template-design .text-gray-500,
.template-design .text-gray-600,
.template-design .text-gray-700 {
  color: white !important;
}
</style>
