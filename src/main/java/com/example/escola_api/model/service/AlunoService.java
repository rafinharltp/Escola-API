package com.example.escola_api.model.service;

import com.example.escola_api.model.entity.Aluno;
import com.example.escola_api.model.repository.AlunoRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class AlunoService {

    private final AlunoRepository alunoRepository;

    public AlunoService(AlunoRepository alunoRepository) {
        this.alunoRepository = alunoRepository;
    }

    public Aluno criarAluno(Aluno aluno) {
        return alunoRepository.save(aluno);
    }

    public List<Aluno> listarAlunos() {
        return alunoRepository.findAll();
    }

    public Optional<Aluno> buscarPorId(Long id) {
        return alunoRepository.findById(id);
    }

    public Aluno atualizarAluno(Long id, Aluno dadosAtualizados) {
        return alunoRepository.findById(id)
                .map(aluno -> {
                    aluno.setNome(dadosAtualizados.getNome());
                    aluno.setEmail(dadosAtualizados.getEmail());
                    aluno.setIdade(dadosAtualizados.getIdade());
                    return alunoRepository.save(aluno);
                })
                .orElseThrow(() -> new RuntimeException("Aluno não encontrado"));
    }

    public void deletarAluno(Long id) {
        alunoRepository.deleteById(id);
    }
}
